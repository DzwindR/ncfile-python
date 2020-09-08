import xarray as xr
import matplotlib.pyplot as plt
import numpy as np

# 解决出图中文和负号显示问题
# 指定默认字体
plt.rcParams['font.sans-serif'] = ['SimHei']
# 解决保存图像是负号'-'显示为方块的问题
plt.rcParams['axes.unicode_minus'] = False

filepath=r"rhum.2016.nc"
nc20=xr.open_dataset(filepath)
# 读取各量
lons=nc20.lon
lats=nc20.lat
levs=nc20.level
times=nc20.time
rhums=nc20.rhum
#数据切片及相关处理
# 选择点位，经纬度（105,30），时间2016.6.14.08-20时
lon=lons[42]
lat=lats[24]
t=times[660:664]
rhum=rhums.isel(lon=42,lat=24,time=[660,661,662,663],level=[0,1,2,3,4,5,6,7])
# 矩阵转置
rh=rhum.T

# 画图
fig=plt.figure(figsize=(10,8))
ax = fig.subplots()
#反转纵轴，使1000hPa作为起点
ax.invert_yaxis()
ax.set_xlabel('时间',fontsize=12)
ax.set_ylabel('层次（hPa）',fontsize=12)
ax.set_yticks([300,500,700,850,925,1000])

plt.xticks(t, ('6-14.08','6-14.14','6-14.20','6-15.00'))

ac=ax.contourf(t,levs,rh,cmap='Greens')

# 色标
cb=fig.colorbar(ac,extend='both',shrink=1,label='相对湿度（%）',pad=0.01)
cb.ax.tick_params(axis='both',which='both',length=1,labelsize=9)
plt.title("时间垂直剖面图",fontsize=16)
plt.savefig("垂直剖面图.png")
plt.show()