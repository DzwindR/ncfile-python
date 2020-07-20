'''
遇到的主要问题是：初次画风，资料的网格很细，风杆严重重叠
                python基本功不扎实，数据的切片不熟练 重点（slice函数）
解决：参考网站：https://unidata.github.io/python-gallery/examples/500hPa_Absolute_Vorticity_winds.htm
                      l#sphx-glr-examples-500hpa-absolute-vorticity-winds-py

'''



import matplotlib.pyplot as plt
import xarray as xr
from scipy.ndimage import gaussian_filter
from mpl_toolkits.basemap import Basemap
import numpy as np
from matplotlib.patches import Polygon
from metpy.units import units
import metpy.calc as mpcalc

#解决出图中文和负号显示问题
plt.rcParams['font.sans-serif'] = ['SimHei'] # 指定默认字体
plt.rcParams['axes.unicode_minus'] = False # 解决保存图像是负号'-'显示为方块的问题
#数据读取及简单处理
file1path=r"16-19_456789.20.nc"
nc20=xr.open_dataset(file1path)
z=nc20.z
u=nc20.u
v=nc20.v
lat=nc20.latitude
lon=nc20.longitude
u_700=u.isel(time=12,level=1)
v_700=v.isel(time=12,level=1)
z_700=z.isel(time=12,level=1)
#地图制作
fig=plt.figure(dpi=220)
ax = plt.gca()
#  左下角的经度和纬度llcrnrlon=80, llcrnrlat=0,
#  右上角的经度和纬度urcrnrlon=140, urcrnrlat=51,
m5=Basemap(llcrnrlon=80, llcrnrlat=15, urcrnrlon=140, urcrnrlat=51, projection='lcc', lat_1=33, lat_2=45, lon_0=104)
m5.readshapefile("CHN_adm_shp//CHN_adm1", 'china', drawbounds=True)    #全国图显示省界
m5.readshapefile("CHN_adm_shp//china-shapefiles-master//china_nine_dotted_line",  'nine_dotted', drawbounds=True)
m5.readshapefile("CHN_adm_shp//CHN_adm3","states", drawbounds=False)   #全国图不显示地级市界（含地级市内容）
lon,lat=np.meshgrid(lon,lat)
x,y=m5(lon,lat)
wind_slice = (slice(None, None, 9), slice(None, None, 9))
cs=m5.barbs(x[wind_slice], y[wind_slice],u_700[wind_slice], v_700[wind_slice],pivot='middle', color='black'
            ,barb_increments={'half':2,'full':4,'flag':20},length=5,alpha=0.8)
m5.drawparallels(np.arange(0, 55., 5.), labels=[1,0,0,0], fontsize=6,linewidth=0.4,alpha=0.8)    #坐标轴为经纬度
m5.drawmeridians(np.arange(70., 140., 5.), labels=[0,0,0,1], fontsize=6,linewidth=0.4,alpha=0.8)
plt.title("ECthin_700hPa_wind_2016.4.13-20",fontsize=6)
m5.drawcoastlines(linewidth=0.25)
m5.drawcountries(linewidth=0.25)
#绘制地级市
for info, shp in zip(m5.states_info, m5.states):
    ziyang=info['NAME_2']
    if ziyang=='Ziyang':
        proid = info['NAME_3']  # 打开CHN_adm12.csv文件，可以知道'NAME_1','NAME_2'代表的名称
        if proid == 'Lezhi':
            poly = Polygon(shp,facecolor='w',edgecolor='k', lw=0.3,alpha=0.2) # 绘制四川省县级市界(乐至)
            ax.add_patch(poly)
            proid1=info['NAME_3']
        if proid=='Anju':
            poly = Polygon(shp, facecolor='w',edgecolor='k', lw=0.3,alpha=0.2)  # 绘制四川省县级市界（安岳）
            ax.add_patch(poly)
        if proid=='Ziyang':
            poly = Polygon(shp, facecolor='w',edgecolor='k', lw=0.3,alpha=0.2)  # 绘制四川省县级市界（雁江）
            ax.add_patch(poly)

#标出宜宾点
Yiblon,Yiblat=np.meshgrid(104.64,28.75)
yibx,yiby=m5(Yiblon,Yiblat)
plt.scatter(yibx,yiby,s=1,c='g')
plt.text(yibx,yiby,'宜宾',fontsize=4,verticalalignment="bottom",horizontalalignment="right")
plt.savefig('photo//700hpa_4.13_20wind_new.png')
plt.show()