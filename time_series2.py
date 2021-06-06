import matplotlib.pyplot as plt
import numpy as np
import xarray as xr
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus']=False
# 资料及要素提取
file1path1=r"../../AllData/2020.78yue_time_seties.nc"
nc1=xr.open_dataset(file1path1)
lons=nc1.longitude
lats=nc1.latitude
levels=nc1.level
rhums=nc1.r
temps=nc1.t
v_winds=nc1.v
u_winds=nc1.u
ws=nc1.w
times=nc1.time

#时间7.10 02时——7.12 08时
time=times[3:12]
# 坐标（104.5 ， 30）   网格分辨率为0.25
lon=lons[138]
lat=lats[120]
parameter={'longitude':138,'latitude':120,'time':np.arange(3,12)}
#输出图片路径名称
outpic=r'../picture/ColdAdvectionForcing/你的图片名称在这里.png'
# 画图
fig=plt.figure(figsize=(16,10))
ax = fig.subplots()
plt.title("图片标题在这里改！！！！！！！！",fontsize=20)

#反转纵轴，使1000hPa作为起点
ax.invert_yaxis()
ax.set_xlabel('时间',fontsize=16)
ax.set_ylabel('层次（hPa）',fontsize=16)
ax.set_yticks([300,500,700,850,925,1000])
# 9个时间点
plt.xticks(time, ('7.10.02','7.10.08','7.10.14','7.10.20','7.11.02','7.11.08','7.11.14','7.11.20','7.12.02'),fontsize=12)

#湿度
# levels=np.arange(40,92,10)是关键，决定了色标上下限，图片显示密度
rhum=rhums.isel(parameter)
rh=rhum.T
ac=ax.contourf(time,levels,rh,cmap='Greens',levels=np.arange(40,100,10),extend='both',zorder=3)
# 色标
cb=fig.colorbar(ac,shrink=1,label='相对湿度（%）',pad=0.02)

#温度
temp0=temps.isel(parameter)
temp_tT=temp0-273.15
temp_t=temp_tT.T
tt=np.arange(-24,36,4)
at=ax.contour(time,levels,temp_t,tt,linewidths=1.2,colors='red',zorder=4)
#零值线加粗，目前想到的本办法
a0=ax.contour(time,levels,temp_t,[0],linewidths=1.4,colors='red',zorder=5)
#fmt参数使标注数字为整数，默认标注3位小数
plt.clabel(at,fontsize=14,fmt='%d',colors="k",inline=True)
#标注0值线
plt.clabel(a0,fontsize=14,fmt='%d',colors="k",inline=True)

#垂直速度
w=ws.isel(parameter)
w=(w.T)*100
aw=ax.contour(time,levels,w,np.arange(-50,50,10),colors='gray',zorder=6)
plt.clabel(aw,fontsize=10,fmt='%d',colors='k',inline=True)

# 经、纬向风
levs=[0,1,2,3,4,5,6,7,8,9,11,13,15,17,19]
lev_list=levels.isel(level=levs)
level={'level':levs}
parameter.update(level)
u_windT=u_winds.isel(parameter)
u_wind=u_windT.T
v_windT=v_winds.isel(parameter)
v_wind=v_windT.T
abar=ax.barbs(time,lev_list,u_wind,v_wind,barb_increments={'half':2,'full':4,'flag':20},zorder=7)

plt.grid(axis="y")
plt.savefig(outpic)
plt.show()