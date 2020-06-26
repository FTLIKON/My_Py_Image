# 基于Python的图片爬虫及图片处理

## 前言
刚刚开始学Python，边学边做的状态~~  
这是一个没有目标的小项目，想到哪就做到哪咯  
这个活还比较有趣，我应该会持续更新的~  

当前进度：  

__1.实现了获取验证码图片的简易爬虫__ 2020/6/25  

__2.实现了图片的二值化与降噪处理__ 2020/6/26

---

### 爬虫：获取验证码图片

~~（其实最开始是想去Pixiv上爬一些妹子的图片的说）~~

因为想要获得大量的，相似有共性的图片，并在后期对这些图片进行深入的处理或者分类，所以想到了：验证码！ 于是我默默的打开了教务系统的页面（狗头保命）：

![教务系统登录界面](https://github.com/FTLIKON/My_Py_Image/blob/master/Blog_Png/1-1.jpg?raw=true)

突然我发现，这个验证码不太一样。很多常见页面的验证码都是点击刷新的，而这里的验证码是每次刷新网页就会刷新。  

暂时不管这个，先常规操作：找到图片的url。 因为我是用的chrome，所以直接右键检查就找到啦。

![找到验证码url](https://github.com/FTLIKON/My_Py_Image/blob/master/Blog_Png/1-2.png?raw=true)

点进去这个url，发现确实是每次刷新网页验证码就会变化！验证了之前的猜想。

![发现验证码特性](https://github.com/FTLIKON/My_Py_Image/blob/master/Blog_Png/1-3.png?raw=true)

那么，利用这个特性，就可以知道爬虫每次访问这个url时获取到的图片都是不同的！那么这个爬虫写起来就相当简单啦！代码如下：

```python

import requests

for i in range(100): # 下载数量，我设置的100
    img_url = "http://passport2.chaoxing.com/num/code?1593027117381"
    r = requests.get(img_url)
    open('image\\%d.png'%i, 'wb').write(r.content) 
    # 二进制写入图片，不存在就新建png文件，并命名为 i.png

```

点击运行！ 和预期一样，在 “/image” 目录下获取了100张验证码，nice！

![获取验证码图片](https://github.com/FTLIKON/My_Py_Image/blob/master/Blog_Png/1-4.png?raw=true)

图片获取成功，接下来则是对图片的处理了。

---

###　图片的二值化与降噪处理  


根据上文的爬虫，已经成功的下载了100 张验证码的图片啦！　但是我发现这些验证码有两个普遍的问题：  

__1.图片清晰度不高，难以辨认__  
__2.噪点过多，难以辨认__  

于是可以通过二值化的操作来先处理清晰度的问题。二值化即为：将图片上的像素点的灰度值设置为0或255，将整个图片呈现出明显的黑白效果。  
这里我学习了一下PIL库，发现有个`getpixel((x,y))`的方法，即为获取坐标值`（x,y）`像素点的RGB颜色值。那么可以设置下二值化的阈值，只保留颜色较深的像素点。代码片段如下：

```python

val = {} # 二值数组
def two_value(image, G): # G: 图像二值化阀值
    for y in range(0, image.size[1]):
        for x in range(0, image.size[0]): # 遍历图片像素点
            g = image.getpixel((x, y))
            if g > G: # 根据阈值二值化
                val[(x, y)] = 1
            else:
                val[(x, y)] = 0

```

这里我发现阈值G设为230最为合适，下面是处理后的效果：  

处理前：  

![处理前](https://github.com/FTLIKON/My_Py_Image/blob/master/Blog_Png/2-1.png?raw=true)
处理后:  

![二值化处理后](https://github.com/FTLIKON/My_Py_Image/blob/master/Blog_Png/2-2.png?raw=true)

可以说效果还是非常好的。但是可以发现依然有一些像素点孤零零的在这些字符外，这些像素点对我们识别图片有害无益。  
这里我通过判断每一个像素点周围相同的像素点的数量，如果相同像素点的数量小于一定数量则可以认为是噪点，删除即可。代码片段如下：

```python

dx = [-1,-1,-1,0,0,1,1,1] # 八个方向，指向相邻的像素点
dy = [-1,0,1,-1,1,1,0,-1]
def clear_noise(image, N): # N: 图片降噪阈值
    val[(0, 0)] = 1
    val[(image.size[0] - 1, image.size[1] - 1)] = 1
    for x in range(1, image.size[0] - 1):
        for y in range(1, image.size[1] - 1):
            nearDots = 0 # 相同像素点的数量
            L = val[(x, y)] # 当前像素点
            for j in range(8): # 和周围8个像素点进行比较
                if L == val[(x + dx[j], y + dy[j])]:
                    nearDots += 1
            if nearDots < N: # 小于阈值，删除像素点
                val[(x, y)] = 0

```

这里的阈值N我发现设置为4最为合适。下面是处理后的效果：
![降噪处理后](https://github.com/FTLIKON/My_Py_Image/blob/master/Blog_Png/2-3.png?raw=true)

效果可以说是非常惊艳了！ 关于保存图片的代码就不分析了，完整代码放在上面的/code文件夹里，需要自取~~