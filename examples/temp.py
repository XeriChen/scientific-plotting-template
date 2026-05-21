import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad
from scipy.optimize import brentq

# 设置中文字体 - 使用系统上已安装的 Noto Sans CJK
plt.rcParams['font.sans-serif'] = ['Noto Sans CJK SC', 'Noto Sans CJK JP', 'Droid Sans Fallback', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# 费米积分 f_m^-(z) = -Li_m(-z) 的数值实现
# 对于 m = 1/2, 3/2
def fermi_integral(m, z):
    """计算 f_m^-(z) = 1/Gamma(m) * ∫_0^∞ x^{m-1}/(exp(x)/z + 1) dx"""
    if z <= 0:
        return 0.0
    # 被积函数
    def integrand(x):
        # 避免溢出：当 x 很大时 exp(x)/z 很大，分母≈exp(x)/z
        # 但被积函数依然数值稳定
        return x**(m-1) / (np.exp(x)/z + 1)
    
    # 积分上限：被积函数主要贡献在 x ~ ln(z) 附近，取足够大的上限
    upper_limit = max(100, 5 * np.log(z + 1) + 20)
    result, _ = quad(integrand, 0, upper_limit, limit=200)
    # 除以 Gamma(m)
    from scipy.special import gamma
    return result / gamma(m)

# 对于非常大的 z，使用渐近展开以避免数值积分困难
def fermi_integral_asymptotic(m, z, terms=2):
    """渐近展开 f_m(z) ~ (ln z)^m / Gamma(m+1) * (1 + pi^2 m(m-1)/(6 (ln z)^2) + ...)"""
    logz = np.log(z)
    # 第一项
    from scipy.special import gamma
    leading = logz**m / (m * gamma(m))  # Gamma(m+1)=m*Gamma(m)
    # 修正项
    correction = 1.0
    if terms >= 2:
        correction += (np.pi**2) * m * (m-1) / (6 * logz**2)
    # 还可以加更高阶项，但这对示意图足够
    return leading * correction

def f_minus(m, z, z_thresh=50):
    """统一接口：小 z 用积分，大 z 用渐近"""
    if z <= z_thresh:
        return fermi_integral(m, z)
    else:
        return fermi_integral_asymptotic(m, z)

# 设定物理参数（无量纲单位）
# 我们选取单位使得特征温度 T0 = 1，此时 z=1 满足 n λ^3 = f_{3/2}(1)
# 定义在 T0 时，热波长 λ = 1/sqrt(T) (设 2πħ^2/(m k_B) = 1)
f32_1 = f_minus(3/2, 1.0)
n = f32_1  # 使得在 T=1 时有 n λ^3 = f_{3/2}(1) -> z=1

# 温度范围 (从远低于 T0 到远高于 T0)
T_vals = np.logspace(-2, 2, 200)  # T/T0 从 0.01 到 100

# 存储结果
chi_vals = []

# 磁化率公式：χ(T) ∝ (1/T) * λ^{-3} * f_{1/2}(z) 忽略常数因子，标度后不变
# λ^{-3} = T^{3/2}，所以 χ(T) ∝ T^{1/2} * f_{1/2}(z)
# 我们直接计算比例值
for T in T_vals:
    # 方程 f_{3/2}(z) = n / λ^3 = n * T^{3/2}
    rhs = n * T**(3/2)
    
    # 确定 z 的搜索范围
    if T > 10:
        # 高温：z 很小，f_{3/2}(z) ≈ z，所以 z ≈ rhs
        z_min = 1e-10
        z_max = max(rhs * 2, 1.0)
    elif T < 0.1:
        # 低温：z 很大
        logz_guess = (rhs * 1.5)**(2/3)
        z_min = max(np.exp(logz_guess * 0.5), 10)
        z_max = np.exp(logz_guess * 2.0)
    else:
        # 中间区域
        z_min = 1e-6
        z_max = 1e6
    
    # 定义方程
    def eq(z):
        return f_minus(3/2, z) - rhs
    
    # 使用 Brent 方法（二分法的改进版，保证收敛）
    try:
        # 确保区间端点的函数值符号相反
        f_min = eq(z_min)
        f_max = eq(z_max)
        
        # 如果符号相同，扩大搜索范围
        if f_min * f_max > 0:
            if f_min > 0:
                # 需要更小的 z_min
                z_min = 1e-20
                f_min = eq(z_min)
            else:
                # 需要更大的 z_max
                z_max = 1e20
                f_max = eq(z_max)
        
        # Brent 方法求解
        z_sol = brentq(eq, z_min, z_max, xtol=1e-12, rtol=1e-12, maxiter=1000)
        
    except Exception as e:
        # 如果仍然失败，使用近似解
        if T > 1:
            z_sol = rhs  # 高温近似 f_{3/2}(z) ≈ z
        else:
            # 低温近似：从渐近展开反推
            logz = (rhs * 1.5)**(2/3)
            z_sol = np.exp(logz)
    
    # 计算 χ 比例值 ∝ T^{1/2} * f_{1/2}(z)
    chi = T**0.5 * f_minus(0.5, z_sol)
    chi_vals.append(chi)

# 归一化到低温极限 χ(0)（取最小温度处的值）
chi0 = chi_vals[0]  # T=0.01 时已经很接近常数
chi_norm = np.array(chi_vals) / chi0

# 绘制示意图
plt.figure(figsize=(8, 5))
plt.loglog(T_vals, chi_norm, 'b-', linewidth=2)
plt.axvline(1.0, color='gray', linestyle='--', alpha=0.5, label=r'$T_0$ (标度温度)')
plt.xlabel(r'$T / T_0$', fontsize=14)
plt.ylabel(r'$\chi(T) / \chi(0)$', fontsize=14)
plt.title('自由电子气的泡利顺磁磁化率', fontsize=15)
plt.grid(True, which='both', linestyle=':', alpha=0.6)
plt.legend()
# 标注区域
plt.text(0.02, 0.95, '低温平台\n(~常数)', transform=plt.gca().transAxes, fontsize=11,
         verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
plt.text(0.7, 0.05, '高温\n居里行为 $\\sim 1/T$', transform=plt.gca().transAxes, fontsize=11,
         verticalalignment='bottom', bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.5))
plt.tight_layout()
plt.savefig('pauli_susceptibility.png', dpi=300, bbox_inches='tight')
plt.savefig('pauli_susceptibility.pdf', bbox_inches='tight')
plt.show()