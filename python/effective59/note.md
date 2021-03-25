## tip14: 優先使用例外，而非回傳None
做錯誤處理時，避免C語言那種依賴回傳值特殊定義(雙方默契)的方式，那不夠明確。

    ret = process()
    if(ret != 0){
        // 錯誤處理
    }

python有兩種建議做法：  
1) 回傳元組：(此方式有比較明確了，但不夠好，因為仍舊依賴了外部函式行為)    

        def divide(a, b):
            try:
                return True, a/b #回傳元組(帶狀態)
            except ZeroDivisionError:
                return False, None #回傳元組(帶狀態)

        success, result = divide(a, b)
        if not success:
            print("error")

 

2) 明確提出例外：  

        def divide(a, b):
            try:
                return a/b
            except ZeroDivisionError as e:
                raise ValueError("divide zero error") as e #明確提出例外
                

        try:
            result = divide(a, b)
        except:
            print("error")
        else:
            print(result)