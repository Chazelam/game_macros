#Requires AutoHotkey v2.0

F12::ExitApp  ; Exit point. F12 stop script
CoordMode "Mouse", "Client"
CoordMode "Pixel", "Client"

; ==================================================
; Constants
; ==================================================

sleepy_time := 1500
sleepy_time_fluctuation := 500
colorTolerance := 15
gamePath := "D:\Games\Punishing Gray Raven\Punishing Gray Raven Game\PGR.exe"
; gamePath := "C:\Punishing Gray Raven\Punishing Gray Raven Game\PGR.exe"

; ==================================================
; Functions
; ==================================================

UserMouseClick(x1, y1, x2, y2) {
    ; Clicks immediately at a random point within the specified rectangle with a delay.
    ;
    ; Parameters:
    ; x1, y1 - Coordinates of the top-left corner of the rectangle.
    ; x2, y2 - Coordinates of the bottom-right corner of the rectangle.
    ;
    ; The function calculates a random point inside the rectangle, moves the mouse to that point,
    ; performs a click, and then applies a random delay.
    delay := Random(sleepy_time - sleepy_time_fluctuation, sleepy_time + sleepy_time_fluctuation)
    x := Random(x1, x2)
    y := Random(y1, y2)

    MouseMove(x, y, Random(10, 100))
    Click()
    Sleep(delay)
}

IsSimilarColor(targetColor, color) {
    ; Determines if two colors are similar based on their RGB values.
    ; Parameters:
    ;   targetColor - The target color in HEX format (e.g., "0xAARRGGBB").
    ;   color       - The color to compare against the target color.
    ; Returns:
    ;   true if the colors are similar, false otherwise.

    ; Extract the red, green, and blue components from the target color
    tr := Format("{:d}", "0x" . substr(targetColor, 3, 2))  ; Red component of targetColor
    tg := Format("{:d}", "0x" . substr(targetColor, 5, 2))  ; Green component of targetColor
    tb := Format("{:d}", "0x" . substr(targetColor, 7, 2))  ; Blue component of targetColor

    ; Extract the red, green, and blue components from the comparison color
    pr := Format("{:d}", "0x" . substr(color, 3, 2))        ; Red component of color
    pg := Format("{:d}", "0x" . substr(color, 5, 2))        ; Green component of color
    pb := Format("{:d}", "0x" . substr(color, 7, 2))        ; Blue component of color

    ; Calculate the Euclidean distance between the two colors in RGB space
    ; Formula: distance = sqrt((R1 - R2)^2 + (G1 - G2)^2 + (B1 - B2)^2)
    distance := sqrt((tr - pr) ** 2 + (tg - pg) ** 2 + (tb - pb) ** 2)

    ; Compare the calculated distance with the predefined tolerance
    if (distance < colorTolerance) {  ; If the distance is less than the tolerance
        return true                   ; The colors are considered similar
    }
    return false                      ; Otherwise, they are not similar
}

; ==================================================
; Login into the Game
; ==================================================
AutoLogin(){
    Run gamePath
    WinWait("PGR")
    WinActivate("PGR")
    
    Sleep(60000)          ; Waiting a loading
    
    ; 30 clicks for login and banners skip
    Loop 30 {
        WinActivate("PGR")
        UserMouseClick(5, 10, 0, 10)
    }
    Sleep(sleepy_time)
}

; ==================================================
; Dorm
; ==================================================
AutoDorm() {
    UserMouseClick(1243, 532, 1243, 532) ; Open Dorm/Guild panel

    UserMouseClick(864, 384, 977, 431)   ; Enter Dorm
    Sleep(10000) ; Wait loading

    UserMouseClick(887, 628, 959, 700)   ; Pat all
    UserMouseClick(887, 628, 959, 700)   ; Confirm
    Sleep(3000)
    ; Commission Tab
    UserMouseClick(1152, 631, 1227, 702) ; Enter tab
    UserMouseClick(25, 601, 125, 694)    ; CLaim All
    UserMouseClick(25, 601, 125, 694)    ; Confirm
    UserMouseClick(25, 601, 125, 694)    ; Dispatch All
    Sleep(5000) ; Wait in case of "already dispatch" pop-up
    Send('{Esc}')
    Sleep(1000)

    ; Chores Tab
    UserMouseClick(1021, 632, 1099, 698) ; Enter Chores Tab
    UserMouseClick(181, 227, 434, 303)   ; Claim Chores
    UserMouseClick(181, 227, 434, 303)   ; Confirm
    UserMouseClick(181, 227, 434, 303)   ; Start Chores
    ; Row 1
    UserMouseClick(245, 180, 465, 270)
    UserMouseClick(515, 180, 745, 270)
    UserMouseClick(795, 180, 1015, 270)
    ; Row 2
    UserMouseClick(245, 315, 465, 400)
    UserMouseClick(515, 315, 745, 400)
    UserMouseClick(795, 315, 1015, 400)
    ; Row 3
    UserMouseClick(245, 452, 471, 533)
    UserMouseClick(515, 447, 743, 533)

    UserMouseClick(867, 619, 1014, 652) ; Begin Chores
    Send('{Esc}')
    Sleep(1000)
    UserMouseClick(214, 656, 317, 681)

    ; ; Shop
    color := PixelGetColor(424, 268)
    if IsSimilarColor(color, "0x125162"){
        UserMouseClick(316, 236, 501, 623)
        UserMouseClick(558, 648, 642, 681)
        UserMouseClick(727, 650, 937, 682)
    }
    Sleep(3000)
    Send('{Esc}')
    Sleep(1000)

    ; Build
    UserMouseClick(41, 647, 171, 684)   ; Open Build Tab
    UserMouseClick(919, 262, 1074, 414) ; Select type
    UserMouseClick(285, 198, 428, 233)  ; Select Floor
    UserMouseClick(896, 611, 1054, 646) ; Confirm
    UserMouseClick(568, 625, 600, 655)  ; +1
    UserMouseClick(568, 625, 600, 655)  ; +1
    UserMouseClick(960, 618, 1180, 655) ; Craft
    UserMouseClick(782, 496, 939, 535)  ; Confirm
    Sleep(5000) ; Wait to complite
    UserMouseClick(782, 496, 939, 535)  ; Confirm if new pop-up

    UserMouseClick(953, 151, 1058, 180) ; Recycle
    UserMouseClick(983, 157, 1006, 175) ; C-Rank
    UserMouseClick(888, 159, 908, 176)  ; B-Rank
    UserMouseClick(787, 158, 808, 174)  ; A-Rank
    UserMouseClick(901, 602, 1051, 634) ; Recycle
    UserMouseClick(901, 602, 1051, 634) ; Confirm
    Send('{Esc}')
    Sleep(1000)

    ; Missions
    UserMouseClick(997, 86, 1231, 131)   ; Open Missions Tab
    UserMouseClick(1072, 123, 1229, 173) ; Claim All
    UserMouseClick(1072, 123, 1229, 173) ; Confirm
    Send('{Esc}')
    Sleep(1000)
    Send('{Esc}')
    Sleep(1000)

}

; ==================================================
; Events
; ==================================================
AutoFreeSerum(){
    UserMouseClick(45, 212, 120, 242)
    Sleep(1000)
    UserMouseClick(60, 607, 122, 672)
    UserMouseClick(60, 607, 122, 672)
    Send('{Esc}')
    Sleep(1000)
} 

; ==================================================
; Guild
; ==================================================
AutoGuild(){
    UserMouseClick(1000, 383, 1135, 442) ; Enter Guild
    Sleep(5000)
    MouseMove(255, 477)
    Click "down"
    Sleep(2000)
    Click "up"
    UserMouseClick(945, 331, 1045, 371)
    Sleep(1000)
    Send('{Esc}')
    Sleep(1000)
    Send('{Esc}')
    Sleep(1000)
}

; ==================================================
; Char shards
; ==================================================
AutoCharShards(){
    UserMouseClick(1068, 306, 1235, 366)
    UserMouseClick(888, 663, 1030, 704)
    UserMouseClick(41, 496, 169, 522)
    MouseMove(398, 416)
    Loop 120{
        MouseClick("WheelUp")
        Sleep(10)
    }
    Sleep(5000)

    ; Bambi
    UserMouseClick(297, 183, 449, 580)
    UserMouseClick(960, 640, 1044, 675)
    UserMouseClick(294, 513, 341, 528)
    UserMouseClick(1025, 505, 1238, 535)
    UserMouseClick(1107, 651, 1219, 679)
    Send('{Esc}')
    Sleep(1000)
    Send('{Esc}')
    Sleep(1000)
    ; Hanung
    UserMouseClick(492, 186, 642, 581)
    UserMouseClick(954, 638, 1045, 676)
    UserMouseClick(296, 509, 356, 535)
    UserMouseClick(1032, 503, 1239, 538)
    UserMouseClick(1101, 652, 1224, 675)
    Send('{Esc}')
    Sleep(1000)
    Send('{Esc}')
    Sleep(1000)

    Send('{Esc}')
    Sleep(1000)
}


; ==================================================
; Top-Up
; ==================================================
AutoTopUp(){
    UserMouseClick(981, 311, 1037, 359) ; Top-Up
    UserMouseClick(495, 95, 591, 120)
    UserMouseClick(46, 261, 153, 282)
    ; Check
    loop 3{
        color := PixelGetColor(338, 322)
        if IsSimilarColor(color, "0xC99344"){
            UserMouseClick(271, 199, 454, 391)
            UserMouseClick(544, 644, 727, 672)
            UserMouseClick(544, 644, 727, 672)
        }
    }
    Send('{Esc}')
    Sleep(1000)
}

; ==================================================
; Serum and missions
; ==================================================
AutoMission(){
    ; if cloer
    UserMouseClick(895, 251, 1038, 282)  ; Enter missions
    UserMouseClick(36, 298, 198, 314)    ; Daily Missions
    UserMouseClick(1076, 125, 1227, 174) ; Claim All
    UserMouseClick(1076, 125, 1227, 174) ; Confirm
    Send('{Esc}')
    Sleep(1000)
    
    UserMouseClick(1073, 179, 1234, 238) ; Events page  
    UserMouseClick(291, 94, 407, 136)    ; Farm Event
    Sleep(1000)

    UserMouseClick(416, 137, 892, 586)
    UserMouseClick(884, 641, 987, 680) ; Auto

    UserMouseClick(1100, 656, 1215, 684) ; Confirm
    Send('{Esc}')
    Sleep(1000)
    Send('{Esc}')
    Sleep(1000)
    Send('{Esc}')
    Sleep(1000)
    
    UserMouseClick(895, 251, 1038, 282)  ; Enter missions
    UserMouseClick(36, 298, 198, 314)    ; Daily Missions
    UserMouseClick(1076, 125, 1227, 174) ; Claim All
    UserMouseClick(1076, 125, 1227, 174) ; Confirm
    UserMouseClick(1178, 623, 1214, 651)
    ; ; BP
    ; UserMouseClick(319, 86, 357, 106)
    ; UserMouseClick(45, 434, 215, 461)
    ; UserMouseClick(996, 646, 1210, 679)
}


; AutoLogin()
WinActivate("PGR")
; AutoDorm()
AutoFreeSerum()
AutoGuild()
AutoTopUp()
AutoCharShards()
AutoMission()
WinClose "PGR"