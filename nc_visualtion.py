'''
参考文献:https://cloud.tencent.com/developer/article/1471314  （xarray数据索引）
        https://unidata.github.io/python-gallery/examples/500hPa_HGHT_Winds.html （画图）
        https://blog.csdn.net/maoye/article/details/90157850 (Basemap地图)
        https://mp.weixin.qq.com/s/CpW0VinslJ1o6dwKDAto6Q (plot基础)
'''
import matplotlib.pyplot as plt
import xarray as xr
from scipy.ndimage import gaussian_filter
from mpl_toolkits.basemap import Basemap
import numpy as np

#解决出图中文和负号显示问题
plt.rcParams['font.sans-serif'] = ['Simsun'] # 指定默认字体
plt.rcParams['axes.unicode_minus'] = False # 解决保存图像是负号'-'显示为方块的问题
#数据读取及简单处理
file1path=r"16-19_456789.20.nc"
nc20=xr.open_dataset(file1path)
z=nc20.z
u=nc20.u
v=nc20.v
lat=nc20.latitude
lon=nc20.longitude
z_500=(gaussian_filter(z.isel(level=0,time=12),sigma=3.0))/98

#地图制作
fig=plt.figure(dpi=300)
m5=Basemap(llcrnrlon=80, llcrnrlat=0, urcrnrlon=140, urcrnrlat=51, projection='lcc', lat_1=33, lat_2=45, lon_0=100)
m5.readshapefile("CHN_adm_shp//china-shapefiles-master//china",  'china', drawbounds=True)
m5.readshapefile("CHN_adm_shp//china-shapefiles-master//china_nine_dotted_line",  'nine_dotted', drawbounds=True)
#m5.readshapefile("CHN_adm_shp//CHN_adm2","CHN_adm2", drawbounds=True)   绘制地级市
lon,lat=np.meshgrid(lon,lat)
x,y=m5(lon,lat)
cs1=m5.contour(x,y,z_500,np.arange(552,588,4),linewidths=0.4,colors='b')       #绘制等高线
cs2 =m5.contour(x, y, z_500,levels=[588],colors='purple',linewidths=0.6)
plt.clabel(cs1,fontsize=5,fmt='%1.0f')                 #等高线标注
plt.clabel(cs2,fontsize=5,fmt='%1.0f')
m5.drawparallels(np.arange(0, 55., 5.), labels=[1,0,0,0], fontsize=6,linewidth=0.4)    #坐标轴为经纬度
m5.drawmeridians(np.arange(70., 140., 10.), labels=[0,0,0,1], fontsize=6,linewidth=0.4)
plt.title("ECthin_500hPa_Higt_2016.4.13-20",fontsize=6)
m5.drawcoastlines(linewidth=0.25)
m5.drawcountries(linewidth=0.25)
lon, lat = m5(104.61, 30.1)
m5.scatter(lon, lat, c='k',s=0.4)
plt.text(lon,lat,r"资阳",fontsize=3.5,verticalalignment='top', horizontalalignment='right',c='red')
plt.savefig('photo//500hpa_4.13_20.png')
plt.show()


