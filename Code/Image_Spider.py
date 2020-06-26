import requests

for i in range(100):
    img_url = "http://passport2.chaoxing.com/num/code?1593027117381"
    r = requests.get(img_url)
    open('image\\%d.png'%i, 'wb').write(r.content)

