class Item: #even een vervanger voor 'resrvaties'
    def __init__(self,a,b):
        self.x1=a
        self.x2=b
        self.P1=20
        self.P2=10
    def change_x1(self,a):
        self.x1=a
    def change_x2(self,a):
        self.x2=a

class ReservatieLijst:
    def __init__(self):
        self.kost=0
        self.lijst=[]
        self.l=len(self.lijst)
        
    def bereken(self):#Kost berekenen
        print '****************kost berekenen **********************'
        self.kost=0
        i=0
        while i<self.l:
            r=self.lijst[i]
            self.kost+= r.x1*r.P1 + r.x2*r.P2
            i+=1
        print 'De kost is momenteel=', self.kost
    
    def voegtoe(self,a):
        self.lijst.append(a)
        self.l+=1
        
    def comp(self,a,b):#kijken wat het verschil zou zijn voor een swap
        print '****************Vergelijk de kost **********************'
        kostA=a.x1*a.P1 + a.x2*a.P2
        kostB=b.x1*b.P1 + b.x2*b.P2
        verschil= kostB-kostA
        print 'vershil:', verschil
        return verschil
    
    def swap(self,a,b):# effectief swappen
        print '****************Swappen **********************'
        i=0
        while i<self.l:
            if self.lijst[i]==a:
                self.lijst[i]=b
                return
            i+=1
        
    
        
def main(): 
    a=Item(0,1)
    b=Item(1,0)
    c=Item(0,1)
    d=Item(0,1)


    k=ReservatieLijst()
    k.voegtoe(a)
    k.voegtoe(b)
    k.voegtoe(c)
    k.voegtoe(d)
    k.bereken()
    if k.comp(b,c)<0:
        k.swap(b,c)
    k.bereken()

main()