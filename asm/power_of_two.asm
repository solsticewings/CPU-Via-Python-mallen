; Determine if a number is a power of two
; R1 = input value (we'll load a constant)
; R2 = R1 - 1
; R3 = R1 & R2
; R4 = result flag (1 = power of two, 0 = not)
; R5 = constant 1
START:
    LOADI   R1, #64         ; test value
    LOADI   R5, #1          ; constant 1
    LOADI   R4, #0          ; assume "not power of two"
LOOP:
    BEQ     R1, #0, DONE    ; if n == 0, skip (0 not power of 2)
    SUB     R2, R1, R5      ; R2 = n - 1
    AND     R3, R1, R2      ; R3 = n & (n - 1)
    BEQ     R3, #0, ISPOW2  ; if n & (n-1) == 0, it’s a power of 2
    B       DONE
ISPOW2:
    LOADI   R4, #1          ; mark "yes"
DONE:
    HALT
