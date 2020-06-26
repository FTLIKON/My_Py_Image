# 基于Python的图片爬虫及图片处理

## 前言
刚刚开始学Python，边学边做的状态~~  
这是一个没有目标的小项目，想到哪就做到哪咯  
这个活还比较有趣，我应该会持续更新的~  

当前进度：  

__1.实现了获取验证码图片的简易爬虫__ 2020/6/25  

__2.实现了验证码的二值化与降噪处理__ 2020/6/26

---

### 爬虫：获取验证码图片

~~（其实最开始是想去Pixiv上爬一些妹子的图片的说）~~

因为想要获得大量的，相似有共性的图片，并在后期对这些图片进行深入的处理或者分类，所以想到了：验证码！ 于是我默默的打开了教务系统的页面（狗头保命）：

![教务系统登录界面](https://github.com/FTLIKON/My_Py_Image/blob/master/pngs/1-1.jpg?raw=true)

突然我发现，这个验证码不太一样。很多常见页面的验证码都是点击刷新的，而这里的验证码是每次刷新网页就会刷新。  

暂时不管这个，先常规操作：找到图片的url。 因为我是用的chrome，所以直接右键检查就找到啦。

![找到验证码url](https://github.com/FTLIKON/My_Py_Image/blob/master/pngs/1-2.png?raw=true)

点进去这个url，发现确实是每次刷新网页验证码就会变化！验证了之前的猜想。

![发现验证码特性](https://github.com/FTLIKON/My_Py_Image/blob/master/pngs/1-3.png?raw=true)

那么，利用这个特性，就可以知道爬虫每次访问这个url时获取到的图片都是不同的！那么这个爬虫写起来就相当简单啦！代码如下：

```python

import requests

for i in range(100): # 下载数量，我设置的100
    img_url = "http://passport2.chaoxing.com/num/code?1593027117381"
    r = requests.get(img_url)
    open('image\\%d.png'%i, 'wb').write(r.content) 
    # 二进制写入图片，不存在就新建png文件，并命名为 i.png

```

点击运行！ 和预期一样，在我的 “/image” 目录下获取了100张验证码，nice！

![获取验证码图片](https://github.com/FTLIKON/My_Py_Image/blob/master/pngs/1-4.png)