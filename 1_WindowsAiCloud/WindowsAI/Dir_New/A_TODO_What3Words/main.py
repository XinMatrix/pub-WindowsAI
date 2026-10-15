import what3words

if __name__ == '__main__':
    geocoder = what3words.Geocoder('F4NF8HMT')
    res = geocoder.convert_to_3wa(what3words.Coordinates(51.484463, -0.195405), language='zh')  # 经纬度转3Words
    print(res)

    # res = geocoder.convert_to_coordinates('邮包.随笔.遥望')  # 3Words转经纬度
    # print(res)
