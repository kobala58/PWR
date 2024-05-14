#include <p16f877a.inc>
__CONFIG _FOSC_EXTRC & _WDTE_OFF & _PWRTE_OFF & _BOREN_OFF & _LVP_ON & _CPD_OFF & _WRT_OFF & _CP_OFF
RES_VECT CODE 0x0000
goto START
MAIN_PROG CODE

START
    ; CONSTS 
    PC   equ  0x02
    PRGFLG equ 0x30

    ; BANK 1
    bcf STATUS, RP1
    bsf STATUS, RP0
    
    ; SETTING PORTS TYPES
    movlw 0x00
    movwf TRISA ;nastaw OUT 
    movwf TRISB ;nastaw OUT 
    movwf TRISD ;7seg disp OUT 
    
    movlw 0xFF
    movwf TRISC ;IN PORT
    
    bcf STATUS, RP0 ;MOVE TO BANK 0
    movlw 0x00
    movwf PORTA
    movlw 0x01
    movwf PORTB

    movlw 0x00
    movwf 0x20	;tmp addr for LED status change
    movlw 0x05	;Set all timers to 5
    
    movwf 0x21	;LED1 CNT
    movwf 0x22	;LED2 CNT
    movwf 0x23	;LED3 CNT
    movwf 0x24	;LED4 CNT
    
    movlw 0x03
    movwf 0x71	;LED1 DEFAULT_CNT
    movwf 0x72	;LED2 DEFAULT_CNT
    movwf 0x73	;LED3 DEFAULT_CNT
    movwf 0x74	;LED4 DEFAULT_CNT
    
    
    

LOOP ;main program loop
    
    CALL LEDCHECK ;Sprawdz co sie dzieje w LEDach
    
    CALL READINPUT
    CALL SELECTCNTADDR
    
    movlw 0xFF 
    movwf 0x25 ;init main timer value
    
    movf 0x20, W 
    movwf PORTA
    
    CALL DRAWFSR ;Wypisz wartosc w wskazniku  
    goto CNT1  
    
; MAIN DELAY INSTRUCTIONS (grabbed from onlinecompiler.com)
      

CNT1
    movlw 0xFF
    movwf 0x26 ;nabij na 0x26 255
    decf 0x25 ; zbij -1 z glownego cntraecf 0x25 ; zbij -1 z glownego cntra
    btfsc STATUS,Z ;sprawdz zerowanie g?ównego cntra
    goto LOOP

CNT2 
    decf 0x26
    btfsc STATUS,Z
    goto CNT1
    goto CNT2
    
; END DELAY INSTRUCTIONG 

SMALLCNT
    movlw 0xFF
    movwf 0x30
    decf 0x30,1
    btfsc STATUS,Z
    goto $-2
    return
    
READINPUT
    btfsc PORTC, 0 ;IN0
    bsf 0x20, 0
    btfsc PORTC, 1 ;IN1
    bsf 0x20, 1
    btfsc PORTC, 2 ;IN2
    bsf 0x20, 2
    btfsc PORTC, 3 ;IN3
    bsf 0x20, 3
    
    btfsc PORTC, 4 ; RIGHT 
    CALL MOVELEFT
    
    btfsc PORTC, 5 ;LEFT 
    CALL MOVERIGHT
    
    btfsc PORTC, 6 ;UP TIME 
    CALL ADDTOCNTR
    
    btfsc PORTC, 7 ;DOWN TIME 
    CALL ADDTOCNTR
    

LEDCHECK
    call LEDCHECK1
;    call LEDCHECK2
;    call LEDCHECK3
;    call LEDCHECK4
    return

LEDCHECK1 ;TODO LEDCHECKI SA DO PRZEROBIENIA, TRZEBA TRZYMAC ODPOWIEDNIA WAROTSC
    decf 0x21, 1
    btfss STATUS,Z
    RETURN
    
    movlw 0x01 ;00000001 do W a potem xorujesz zeby flipnac tylko 1 bit
    xorwf  0x20,1
    movf 0x71, W
    movwf 0x21
    RETURN
    


MOVELEFT
    RLF PORTB, 1
    btfss PORTB, 4 ;check if we are 5th led if that 
    RETURN
    movlw 0x01
    movwf PORTB
    BSF PRGFLG,1
    RETURN
    
MOVERIGHT
    RRF PORTB,1
    btfss STATUS, C
    RETURN
    BCF STATUS, C
    movlw 0x08
    movwf PORTB
    BSF PRGFLG,1
    RETURN

SELECTCNTADDR
    btfsc PORTB,0
    movlw 0x71
    btfsc PORTB,1
    movlw 0x72
    btfsc PORTB,2
    movlw 0x73
    btfsc PORTB,3
    movlw 0x74
    movwf FSR ;load selected memory to fsr pointer
    RETURN 
    
ADDTOCNTR 
    INCF INDF,1
;    movlw 0x09
;    movwf INDF
    call DRAWFSR
    
    btfsc PORTC, 6
    goto ADDTOCNTR
    
   RETURN 

SUBFROMCNTR
   decf INDF,1
   
   
REMOVEOVERFLOW
   movf INDF,W
   sublw d'10'
   btfss STATUS,Z; W = 10 skip jesli INDF == 10
   RETURN
   movlw 0x00 ; if one digit was over 9, assign 0
   movwf INDF 
   bsf PRGFLG,1 ;set flag to notice that some val was changed
   RETURN
   
   
DRAWFSR ;we need to ensure that 
    movf INDF,W
    call table
    movwf PORTD
    RETURN
    
table addwf   PC
    retlw  0x7E
    retlw  0x0C
    retlw  0xB6
    retlw  0x9E
    retlw  0xCC
    retlw  0xDA
    retlw  0xFA
    retlw  0x0E
    retlw  0xFE
    retlw  0xCE
    return 
    
end
