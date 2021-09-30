(declare-fun TPD7 () Int)
(declare-fun TPD6 () Int)
(declare-fun TPD5 () Int)
(declare-fun TPD4 () Int)
(declare-fun TPD3 () Int)
(declare-fun TPD2 () Int)
(declare-fun TPD1 () Int)
(declare-fun TPD0 () Int)
(declare-fun TPC7 () Int)
(declare-fun TPC6 () Int)
(declare-fun TPC5 () Int)
(declare-fun TPC4 () Int)
(declare-fun TPC3 () Int)
(declare-fun TPC2 () Int)
(declare-fun TPC1 () Int)
(declare-fun TPC0 () Int)
(declare-fun TPS7 () Int)
(declare-fun TPS6 () Int)
(declare-fun TPS5 () Int)
(declare-fun TPS4 () Int)
(declare-fun TPS3 () Int)
(declare-fun TPS2 () Int)
(declare-fun TPS1 () Int)
(declare-fun TPS0 () Int)
(declare-fun TPN7 () Int)
(declare-fun TPN6 () Int)
(declare-fun TPN5 () Int)
(declare-fun TPN4 () Int)
(declare-fun TPN3 () Int)
(declare-fun TPN2 () Int)
(declare-fun TPN1 () Int)
(declare-fun TPN0 () Int)
(declare-fun TPP0 () Int)
(declare-fun TPP1 () Int)
(declare-fun TPP2 () Int)
(declare-fun TPP3 () Int)
(declare-fun TPP4 () Int)
(declare-fun TPP5 () Int)
(declare-fun TPP6 () Int)
(declare-fun TPP7 () Int)
(assert (and (= (+ TPN0 TPN1 TPN2 TPN3 TPN4 TPN5 TPN6 TPN7) 4)
     (= (+ TPS0 TPS1 TPS2 TPS3 TPS4 TPS5 TPS6 TPS7) 8)
     (= (+ TPC0 TPC1 TPC2 TPC3 TPC4 TPC5 TPC6 TPC7) 10)
     (= (+ TPD0 TPD1 TPD2 TPD3 TPD4 TPD5 TPD6 TPD7) 20)))
(assert (>= TPN0 0))
(assert (>= TPP0 0))
(assert (>= TPS0 0))
(assert (>= TPC0 0))
(assert (>= TPD0 0))
(assert (<= (+ (* TPN0 700) (* TPP0 400) (* TPS0 1000) (* TPC0 2500) (* TPD0 200)) 8000))
(assert (<= (+ TPN0 TPP0 TPS0 TPC0 TPD0) 8))
(assert (<= TPN0 1))
(assert (=> (> TPP0 0) (= TPC0 0)))
(assert (=> (> TPC0 0) (= TPP0 0)))
(assert (>= TPN1 0))
(assert (>= TPP1 0))
(assert (>= TPS1 0))
(assert (>= TPC1 0))
(assert (>= TPD1 0))
(assert (<= (+ (* TPN1 700) (* TPP1 400) (* TPS1 1000) (* TPC1 2500) (* TPD1 200)) 8000))
(assert (<= (+ TPN1 TPP1 TPS1 TPC1 TPD1) 8))
(assert (<= TPN1 1))
(assert (=> (> TPP1 0) (= TPC1 0)))
(assert (=> (> TPC1 0) (= TPP1 0)))
(assert (>= TPN2 0))
(assert (>= TPP2 0))
(assert (>= TPS2 0))
(assert (>= TPC2 0))
(assert (>= TPD2 0))
(assert (<= (+ (* TPN2 700) (* TPP2 400) (* TPS2 1000) (* TPC2 2500) (* TPD2 200)) 8000))
(assert (<= (+ TPN2 TPP2 TPS2 TPC2 TPD2) 8))
(assert (<= TPN2 1))
(assert (=> (> TPP2 0) (= TPC2 0)))
(assert (=> (> TPC2 0) (= TPP2 0)))
(assert (>= TPN3 0))
(assert (>= TPP3 0))
(assert (>= TPS3 0))
(assert (>= TPC3 0))
(assert (>= TPD3 0))
(assert (<= (+ (* TPN3 700) (* TPP3 400) (* TPS3 1000) (* TPC3 2500) (* TPD3 200)) 8000))
(assert (<= (+ TPN3 TPP3 TPS3 TPC3 TPD3) 8))
(assert (<= TPN3 1))
(assert (=> (> TPP3 0) (= TPC3 0)))
(assert (=> (> TPC3 0) (= TPP3 0)))
(assert (= TPS3 0))
(assert (>= TPN4 0))
(assert (>= TPP4 0))
(assert (>= TPS4 0))
(assert (>= TPC4 0))
(assert (>= TPD4 0))
(assert (<= (+ (* TPN4 700) (* TPP4 400) (* TPS4 1000) (* TPC4 2500) (* TPD4 200)) 8000))
(assert (<= (+ TPN4 TPP4 TPS4 TPC4 TPD4) 8))
(assert (<= TPN4 1))
(assert (=> (> TPP4 0) (= TPC4 0)))
(assert (=> (> TPC4 0) (= TPP4 0)))
(assert (= TPS4 0))
(assert (>= TPN5 0))
(assert (>= TPP5 0))
(assert (>= TPS5 0))
(assert (>= TPC5 0))
(assert (>= TPD5 0))
(assert (<= (+ (* TPN5 700) (* TPP5 400) (* TPS5 1000) (* TPC5 2500) (* TPD5 200)) 8000))
(assert (<= (+ TPN5 TPP5 TPS5 TPC5 TPD5) 8))
(assert (<= TPN5 1))
(assert (=> (> TPP5 0) (= TPC5 0)))
(assert (=> (> TPC5 0) (= TPP5 0)))
(assert (= TPS5 0))
(assert (>= TPN6 0))
(assert (>= TPP6 0))
(assert (>= TPS6 0))
(assert (>= TPC6 0))
(assert (>= TPD6 0))
(assert (<= (+ (* TPN6 700) (* TPP6 400) (* TPS6 1000) (* TPC6 2500) (* TPD6 200)) 8000))
(assert (<= (+ TPN6 TPP6 TPS6 TPC6 TPD6) 8))
(assert (<= TPN6 1))
(assert (=> (> TPP6 0) (= TPC6 0)))
(assert (=> (> TPC6 0) (= TPP6 0)))
(assert (= TPS6 0))
(assert (>= TPN7 0))
(assert (>= TPP7 0))
(assert (>= TPS7 0))
(assert (>= TPC7 0))
(assert (>= TPD7 0))
(assert (<= (+ (* TPN7 700) (* TPP7 400) (* TPS7 1000) (* TPC7 2500) (* TPD7 200)) 8000))
(assert (<= (+ TPN7 TPP7 TPS7 TPC7 TPD7) 8))
(assert (<= TPN7 1))
(assert (=> (> TPP7 0) (= TPC7 0)))
(assert (=> (> TPC7 0) (= TPP7 0)))
(assert (= TPS7 0))
(maximize (+ TPP0 TPP1 TPP2 TPP3 TPP4 TPP5 TPP6 TPP7))
(check-sat)

sat
[TPC6 = 2,
 TPN2 = 1,
 TPN1 = 0,
 TPN6 = 1,
 TPS2 = 2,
 TPD3 = 5,
 TPD2 = 1,
 TPD4 = 0,
 TPD5 = 0,
 TPN5 = 0,
 TPC5 = 0,
 TPP2 = 0,
 TPP6 = 0,
 TPP0 = 0,
 TPP7 = 0,
 TPP4 = 8,
 TPC2 = 2,
 TPN4 = 0,
 TPN3 = 1,
 TPD6 = 5,
 TPS1 = 4,
 TPN7 = 1,
 TPC4 = 0,
 TPP3 = 0,
 TPD1 = 0,
 TPC3 = 2,
 TPD7 = 5,
 TPP1 = 4,
 TPC7 = 2,
 TPP5 = 8,
 TPC1 = 0,
 TPS7 = 0,
 TPS6 = 0,
 TPS5 = 0,
 TPS4 = 0,
 TPS3 = 0,
 TPD0 = 4,
 TPC0 = 2,
 TPS0 = 2,
 TPN0 = 0]
