import urllib.request, re, html

url = "https://books.toscrape.com/"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
page = urllib.request.urlopen(req, timeout=25).read().decode("utf-8")

for art in re.findall(r'<article class="product_pod">(.*?)</article>', page, re.S)[:6]:
    title = re.search(r'<h3><a[^>]*title="([^"]+)"', art).group(1)
    price = re.search(r'price_color">([^<]+)', art).group(1)
    stars = re.search(r'star-rating (\w+)', art).group(1)
    print(html.unescape(title), "|", price, "|", stars, "stars")
