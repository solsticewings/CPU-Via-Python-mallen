; Euclid's GCD algorithm
START:
    LOADI R6, #0xFF
    CALL GCD
    HALT
GCD:
    BEQ R2, #0, DONE
    SUB R1, R1, R2
    BNE R1, #0, GCD
DONE:
    RET
