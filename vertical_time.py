import matplotlib.pyplot as plt
import numpy as np
import xarray as xr

#显示中文
plt.rcParams['font.sans-serif'] = ['SimHei']
#用来正常显示负号
plt.rcParams['axes.unicode_minus']=False

filepath1=r"2016.06.nc"
filepath2=r"2016.06.U.nc"
nc1=xr.open_dataset(filepath1)
nc2=xr.open_dataset(filepath2)

lons=nc1.longitude
lats=nc1.latitude
times=nc1.time
levs=nc1.level
rhums=nc1.r
temps=nc1.t
v_winds=nc1.v
u_winds=nc2.u

lon=lons[46]
lat=lats[80]
time=times[52:76]

tarray=np.arange(52,76)
rhum=rhums.isel(longitude=46,latitude=80,time=tarray)
rh=rhum.T

# 画图
fig=plt.figure(figsize=(20,12))
ax = fig.subplots()
#湿度
#反转纵轴，使1000hPa作为起点
ax.invert_yaxis()
ax.set_xlabel('时间',fontsize=12)
ax.set_ylabel('层次（hPa）',fontsize=12)
ax.set_yticks([300,500,700,850,925,1000])

plt.xticks(time, ('6-14.08','6-14.14','6-14.20','6-15.00'))

# levels=np.arange(40,92,10)是关键，决定了色标上下限，图片显示密度
ac=ax.contourf(time,levs,rh,cmap='Greens',levels=np.arange(40,92,10),extend='both',zorder=3)
# 色标
cb=fig.colorbar(ac,extend='both',shrink=1,label='相对湿度（%）',pad=0.01)


#温度
temp0=temps.isel(longitude=46,latitude=80,time=tarray)
temp_tT=temp0-273.15
temp_t=temp_tT.T
tt=np.arange(-20,32,4)
at=ax.contour(time,levs,temp_t,tt,linewidths=1,colors='red',zorder=4)
#零值线加粗，目前想到的本办法
a0=ax.contour(time,levs,temp_t,[0],linewidths=1.3,colors='red',zorder=5)
#fmt参数使标注数字为整数，默认标注3位小数
plt.clabel(at,fontsize=11,fmt='%d',colors="k",inline=True)
#标注0值线
plt.clabel(a0,fontsize=11,fmt='%d',colors="k",inline=True)

#经、纬向风
lev_list=levs.isel(level=[0,4,8,12,16])
u_windT=u_winds.isel(longitude=46,latitude=80,level=[0,4,8,12,16],time=tarray)
u_wind=u_windT.T

v_windT=v_winds.isel(longitude=46,latitude=80,level=[0,4,8,12,16],time=tarray)
v_wind=v_windT.T
abar=ax.barbs(time,lev_list,u_wind,v_wind,barb_increments={'half':2,'full':4,'flag':20},length=6,zorder=6)

plt.grid(axis="y")
plt.title("EC - 时间垂直\n(104.5 , 30)                                             "
          "                                    2016.6.14.08")
plt.show()