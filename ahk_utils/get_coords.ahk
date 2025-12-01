#Requires AutoHotkey v2.0

; name := "Александр"
; age := 25
; message := "mouseC" . name . " и мне " . age . " лет.`n"
; filePath := "output.txt"  ; Путь к файлу
; FileAppend(message, filePath)
; MsgBox("Текст успешно записан в файл: " . filePath)

detectCord(){
    MouseGetPos &xpos, &ypos 
    WinGetPos &OutX, &OutY, &OutWidth, &OutHeight, 'Калькулятор'

    MsgBox "The cursor is at X" OutX " Y" OutY "`nThe cursor is at X" xpos " Y" ypos
}
; Функция для проверки цвета пикселя
CheckPixelColor() {
    ; Получаем цвет пикселя в указанной позиции
    MouseGetPos &x, &y
    color := PixelGetColor(x, y)

    ; Выводим результат
    MsgBox("Цвет пикселя в точке (" . x . ", " . y . ") = " . color)
}
detectStartCord(){
    global x1 
    global y1
    MouseGetPos &x1, &y1
}
detectEndCord(){
    global x1
    global y1
    MouseGetPos &x2, &y2
    
    filePath := "output.txt"  ; Путь к файлу
    FileAppend("UserMouseClick(" . x1 . ", " . y1 . ", " . x2 . ", " . y2 . ")`n", filePath)
}

F1::detectStartCord()
F2::detectEndCord()

; Пример: Проверяем цвет пикселя в координатах мыши
F3::CheckPixelColor()
