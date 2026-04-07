; Demonstrate SHFT (shift left/right) and OR operations
; R1 and R2 are source registers
; R3 and R4 store intermediate results
; R5 stores final OR result

START:
    LOADI  R1, #0x03      ; R1 = 0000 0000 0000 0011
    LOADI  R2, #0x02      ; R2 = 0000 0000 0000 0010
    SHFT   R3, R1, R2     ; R3 = R1 << R2  = 0000 0000 0000 1100
    SUB    R2, R0, R2     ; R2 = 0 - 2 = -2
    SHFT   R4, R3, R2     ; R4 = R3 >> 2   = 0000 0000 0000 0011
    OR     R5, R3, R4     ; R5 = R3 | R4   = 0000 0000 0000 1111
END:
    HALT                  ; Stop execution