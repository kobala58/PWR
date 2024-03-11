#include <p16f877a.inc>
__CONFIG _FOSC_EXTRC & _WDTE_OFF & _PWRTE_OFF & _BOREN_OFF & _LVP_ON & _CPD_OFF & _WRT_OFF & _CP_OFF
RES_VECT CODE 0x0000
goto START
MAIN_PROG CODE

START
    bcf STATUS, RP1
    bsf STATUS, RP0
    movlw 0x00
    movwf TRISA ;nastaw 
    movlw 0xFF
    movwf TRISC
    bcf STATUS, RP0
    movlw 0x00
    movwf PORTA

    movlw 0x00
    movwf 0x20
    movlw 0x05	;Set all timers to 5
    movwf 0x21	;LED1 CNT
    movwf 0x22	;LED2 CNT
    movwf 0x23	;LED3 CNT
    movwf 0x24	;LED4 CNT
    
    movlw 0xFF
    movwf 0x25 ;init main timer value

LOOP
    CALL LEDCHECK1
    btfsc PORTC, 0
    bsf 0x20, 0
    btfsc PORTC, 1
    bsf 0x20, 1
    btfsc PORTC, 2
    bsf 0x20, 2
    btfsc PORTC, 3
    bsf 0x20, 3
    movf 0x20, W
    movwf PORTA
    CALL LEDCHECK
    goto CNT1    

CNT1
    movlw 0xFF
    movwf 0x26 ;nabij na 0x26 255
    decf 0x25 ; zbij -1 z glownego cntra
    btfsc STATUS,Z ;sprawdz zerowanie głównego cntra
    goto LOOP

CNT2 
    decf 0x26
    btfsc STATUS,Z
    goto CNT1
    goto CNT2

LEDCHECK
    call LEDCHECK1
    call LEDCHECK2
    call LEDCHECK3
    call LEDCHECK4
    return

LEDCHECK1
    btfsc 0x20, 0
    decf 0x21
    btfss STATUS,Z
    RETURN
    
    bcf 0x20, 0
    movlw 0x05
    movwf 0x21
    RETURN
    
LEDCHECK2
    btfsc 0x20, 1
    decf 0x22
    btfss STATUS,Z
    RETURN
    
    bcf 0x20, 1
    movlw 0x05
    movwf 0x22
    RETURN
    
LEDCHECK3
    btfsc 0x20, 2
    decf 0x23
    btfss STATUS,Z
    RETURN
    
    bcf 0x20, 2
    movlw 0x05
    movwf 0x23
    RETURN
    
LEDCHECK4
    btfsc 0x20, 3
    decf 0x24
    btfss STATUS,Z
    RETURN
    
    bcf 0x20, 3
    movlw 0x05
    movwf 0x24
    RETURN

end
