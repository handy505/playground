'''
使用產生式的時機：(範列：找出每個字索引位置)
index_words()使用串列處理，在函式內建立好串列後回傳。
使用串列的缺點：
1) 視覺雜訊大，雖然python的內建串列已經好進步，但仍被嫌了。(C語言哭哭~)
2) 大檔案輸入時，對記憶體的耗損重。
'''
def index_words(text):
    result = []
    if text:
        result.append(0)
    for index, letter in enumerate(text):
        if letter == ' ':
            result.append(index+1)
    return result


'''
改用產生式(yield)後，視覺雜訊降低了，但外層要多做一個轉串列處理
'''
def index_words_iter(text):
    result = []
    if text:
        yield 0
    for index, letter in enumerate(text):
        if letter == ' ':
            yield index + 1    


address = "Four score and seven years ago..."
result = index_words(address)
print(result[:3])

result = list(index_words_iter(address))
print(result[:3])
