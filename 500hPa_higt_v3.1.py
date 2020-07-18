'''
参考文献:https://cloud.tencent.com/developer/article/1471314  （xarray数据索引）
        https://unidata.github.io/python-gallery/examples/500hPa_HGHT_Winds.html （画图）
        https://blog.csdn.net/maoye/article/details/90157850 (Basemap地图)
        https://mp.weixin.qq.com/s/CpW0VinslJ1o6dwKDAto6Q (plot基础)
        https://www.zhihu.com/question/49669755 （利用shp画地级市轮廓）
        感谢以上文献作者！！！
'''
import matplotlib.pyplot as plt
import xarray as xr
from scipy.ndimage import gaussian_filter
from mpl_toolkits.basemap import Basemap
import numpy as np
from matplotlib.patches import Polygon

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
z_500=(gaussian_filter(z.isel(level=0,time=12),sigma=3.0))/98

#地图制作
fig=plt.figure(dpi=300)
ax = plt.gca()
#  左下角的经度和纬度llcrnrlon=80, llcrnrlat=0,
#  右上角的经度和纬度urcrnrlon=140, urcrnrlat=51,

m5=Basemap(llcrnrlon=80, llcrnrlat=15, urcrnrlon=140, urcrnrlat=51, projection='lcc', lat_1=33, lat_2=45, lon_0=100)
m5.readshapefile("CHN_adm_shp//CHN_adm1", 'china', drawbounds=True)    #全国图显示省界
m5.readshapefile("CHN_adm_shp//china-shapefiles-master//china_nine_dotted_line",  'nine_dotted', drawbounds=True)
m5.readshapefile("CHN_adm_shp//CHN_adm3","states", drawbounds=False)   #全国图不显示地级市界（含地级市内容）
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
#绘制地级市
for info, shp in zip(m5.states_info, m5.states):
    sheng=info['NAME_2']
    proid = info['NAME_3']  # 打开CHN_adm12.csv文件，可以知道'NAME_1','NAME_2'代表的名称
    if (proid == 'Lezhi' and sheng=='Ziyang'):
        poly = Polygon(shp,facecolor='w',edgecolor='k', lw=0.3) # 绘制四川省县级市界(乐至)
        ax.add_patch(poly)
    if (proid=='Anju'and sheng=='Ziyang'):
        poly = Polygon(shp, facecolor='w',edgecolor='k', lw=0.3)  # 绘制四川省县级市界（安岳）
        ax.add_patch(poly)
    if (proid=='Ziyang'and sheng=='Ziyang'):
        poly = Polygon(shp, facecolor='w',edgecolor='k', lw=0.3)  # 绘制四川省县级市界（雁江）
        ax.add_patch(poly)

#标出宜宾点
Yiblon,Yiblat=np.meshgrid(104.64,28.75)
yibx,yiby=m5(Yiblon,Yiblat)
plt.scatter(yibx,yiby,s=1,c='g')
plt.text(yibx,yiby,'宜宾',fontsize=4,verticalalignment="bottom",horizontalalignment="right")
plt.savefig('photo//500hpa_4.13_20_new.png')
plt.show()