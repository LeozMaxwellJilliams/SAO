'''
FinalProject.py
Leon Ouyang and Andy Li
This is a game we made based on the anime Sword Art Online. You must clear 4
dungeons by beating each dungeon's boss in order to beat the game. You can
level up and gain new skills along the way
'''

from pygame import *
from random import *
from math import *

size = width, height = 1200,790
screen = display.set_mode(size)

font.init()

#initiating fonts that i use 
comicFont=font.SysFont("Comic Sans MS", 20)
arialFont=font.SysFont("Arial",14)
arialFont2=font.SysFont("Arial",12)

class portal(): #stores information about portals going from map to map
    def __init__(self,info):

        self.coord = [info[0],info[1]]
        info = list(map(int,info))

        self.ncoord = [info[2],info[3]]
        self.rect = Rect(info[0],info[1],info[4],info[5])
        self.length = info[4]
        self.height = info[5]
        self.newmap = info[6]
        
    def collision(self,x,y): #Checks if player if touching the portal
        return self.rect.collidepoint(x,y)
    
    def getspot(self): #Gives the new coordinates of the ball to go to.
        return self.ncoord[0],self.ncoord[1]


class MAP():
    def __init__(self, stage, mapnum):
        self.stage = stage #which dungeons you're on
        self.portals=[] #portals of the map you're in
        self.load(str(mapnum)) #loading the map you're in
        self.mapnum=mapnum #which map you're in
        #when the player dies his stats go back to these save stats
        self.savehp = 500
        self.savemp = 100
        self.saveatk = 20
        self.savedefence = 30
        self.saveexp = 0
        self.savelevel = 1
        self.savex = 300
        self.savey = 400
        self.savemapnum = "10"
        self.savestage = ""

    def load(self,mapnum): #Function to reload all the map data ( images, mask, new portals ) after a map has been switched
        mapnum = str(mapnum)
        self.mapnum=mapnum
        self.level = image.load("MAP MOVE/maps"+self.stage+"/"+mapnum+".png")
        self.mask = image.load("MAP MOVE/maps"+self.stage+"/"+mapnum+"_m.png")
        self.sizex, self.sizey = self.level.get_size()
        
        infile = open("MAP MOVE/mapinfo"+self.stage+"/map"+mapnum+".txt","r")
        num = infile.readline().strip().split()
        self.portals = []
        for i in range(int(num[0])):
            info = infile.readline().strip().split()
            self.portals.append(portal(info))
        infile.close()
        
        infile = open("MAP MOVE/mapinfo"+self.stage+"/spawn"+mapnum+".txt","r")
        spawn = infile.read().strip().split()
        self.spawnx = [x.split(',')[0] for x in spawn]
        self.spawny = [y.split(',')[1] for y in spawn]
        try:
            self.limit = int(spawn[0].split(',')[2])
        except:
            self.limit = 0
        self.spawnloc = [(int(self.spawnx[i]),int(self.spawny[i])) for i in
                              range(len(self.spawnx))]
        infile.close()

    def loadmonsters(self): #loads all the monsters in the dungeons you're in
        infile = open("MAP MOVE/monsters"+self.stage+".txt","r")
        monsters = infile.read().strip().split()
        self.monsters=[]
        self.spawnmaps=[]
        for i in monsters:
            monster=i.split(',')
            #creates an instance of each monster
            self.monsters.append(Enemy(int(monster[0]),int(monster[1]),int(monster[2])
                                       ,int(monster[3]),int(monster[4]),int(monster[5])
                                       ,loadsheet2(monster[6],4,int(monster[21]))+loadsheet2(monster[7],4,int(monster[21]))
                                       ,0,0,[int(monster[8]),int(monster[9]),int(monster[10]),
                                             int(monster[11]),int(monster[12]),int(monster[13]),
                                             int(monster[14]),int(monster[15])],int(monster[16])
                                       ,int(monster[17]),int(monster[18]),int(monster[19]),monster[20],int(monster[21])))

            self.spawnmaps.append(monster[22:len(i)-1]) #records what map each monster spawns in
            
        infile.close()

    def draw(self,player,monsters): #draws everything in the map
        #(player you are drawing,list of monsters that are alive)
       
        mapRect=Rect(self.mapx,self.mapy, 1200,700)
        screen.blit(self.level.subsurface(self.mapx,self.mapy, 1200,700),(0,0))
        #blits the subsurface of the map you see(the background)

        for monster in monsters: #draws all the monsters
            if monster.Rect.colliderect(mapRect):
                mx=monster.x-self.mapx
                my=monster.y-self.mapy

                screen.blit(monster.image[monster.direct][int(monster.frame)],
                            (mx-monster.wid,my-monster.hi))
                monster.hpbar(self.mapx,self.mapy)

        #there is a different offset when blitting on the player for some
        #skills so i fix it here then i blit the player
        pic=player.image[player.direct][player.action][int(player.frame)]
        if player.action==ray:
            screen.blit(pic,(self.sx-player.wid,self.sy-player.hi-35))
        elif player.action==pierce:
            if player.direct==right:
                screen.blit(pic,(self.sx-player.wid+185,self.sy-player.hi))
            if player.direct==left:
                screen.blit(pic,(self.sx-player.wid-185,self.sy-player.hi))
            if player.direct==down:
                screen.blit(pic,(self.sx-player.wid,self.sy-player.hi+185))
            if player.direct==up:
                screen.blit(pic,(self.sx-player.wid,self.sy-player.hi-185))
        elif player.action==slash:
            if player.direct==right:
                screen.blit(pic,(self.sx-player.wid+120,self.sy-player.hi))
            if player.direct==left:
                screen.blit(pic,(self.sx-player.wid-120,self.sy-player.hi))
            if player.direct==down:
                screen.blit(pic,(self.sx-player.wid,self.sy-player.hi+120))
            if player.direct==up:
                screen.blit(pic,(self.sx-player.wid,self.sy-player.hi-120))
        elif player.action==blast:
            if player.direct==right:
                screen.blit(pic,(self.sx-player.wid+375,self.sy-player.hi))
            if player.direct==left:
                screen.blit(pic,(self.sx-player.wid-375,self.sy-player.hi))
            if player.direct==down:
                screen.blit(pic,(self.sx-player.wid,self.sy-player.hi+375))
            if player.direct==up:
                screen.blit(pic,(self.sx-player.wid,self.sy-player.hi-375))
        else:
            screen.blit(pic,(self.sx-player.wid,self.sy-player.hi))

        #bliting the information panel at the bottom of the screen
        screen.blit(khead,(5,700))
        screen.blit(mapinfo,(0,115))

        txt=arialFont2.render(str(player.level),True,(255,255,255))
        screen.blit(txt,(65,760))
        txt=arialFont.render("Kirito",True,(255,255,255))
        screen.blit(txt,(90,700))
        txt=arialFont.render("Level "+str(player.level),True,(255,255,255))
        screen.blit(txt,(90,715))
        txt=arialFont2.render(str(player.atk),True,(255,255,255))
        screen.blit(txt,(95,753))
        txt=arialFont2.render(str(player.defence),True,(255,255,255))
        screen.blit(txt,(123,753))

        player.hpbar(250,710,261,13)
        player.mpbar(250,750,261,13)
        player.expbar(605,745,261,13)
        drawicons(player)

    def check(self,px,py): #checks if you can walk to the next point
        try:
            check = self.mask.get_at((px, py)) # checks if the next spot is white and/or red or not, if not then position remains the same
        except:
            return True
        if check[:3] != (255,255,255) and check[:3] != (255,0,0) :
            return True
        return False

    def savecheck(self,player): #checks if you're at a save crystal
        check = self.mask.get_at((player.x,player.y))
        if check[:3] == (255,0,0): #updates all the save stats if you are
            self.savehp = player.tothp
            self.savemp = player.totmp
            self.saveatk = player.atk
            self.savedefence = player.defence
            self.saveexp = player.exp
            self.savelevel = player.level
            self.savex = player.x
            self.savey = player.y
            self.savemapnum = self.mapnum
            self.savestage = self.stage
            player.hp+=1 #heals you too
            if player.hp>player.tothp:
                player.hp = player.tothp
    
    def portalcheck(self,player): #Checks if the player is at a portal or not, If it is, initiated transfer function
        for portal in self.portals:
            if portal.collision(player.x,player.y):
                self.transfer(portal,kirito)
                break

    def transfer(self,portal,player): #Sets new coordinates for the player. And loads in the new map.
        player.x,player.y = portal.getspot()
        self.load(portal.newmap)
        #deletes old monsters and damage numbers
        del alive[:]
        del dmgs[:]
        del dmgposx[:]
        del dmgposy[:]
        del dmgmapx[:]
        del dmgmapy[:]
        del dmgtimes[:]
        del dmgalpha[:]
        del dmgpic[:]
        self.maptoscreen(player.x,player.y)

    def bosstransfer(self,player): #transfers from one dungeons to the next
        #after you beat the boss
        if self.stage=="":
            self.stage="2"
            self.mapnum="1"
            self.load("1")
            player.x,player.y=2200,500
            self.loadmonsters()
            storyparts(2,4)
        elif self.stage=="2":
            self.stage="3"
            self.mapnum="1"
            self.load("1")
            player.x,player.y=500,700
            self.loadmonsters()
            storyparts(2,6)
        elif self.stage=="3":
            self.stage="4"
            self.mapnum="1"
            self.load("1")
            player.x,player.y=1295,1550
            self.loadmonsters()
            storyparts(2,8)

        self.maptoscreen(player.x,player.y)
        del alive[:]
        del dmgs[:]
        del dmgposx[:]
        del dmgposy[:]
        del dmgmapx[:]
        del dmgmapy[:]
        del dmgtimes[:]
        del dmgalpha[:]
        del dmgpic[:]
        player.action = 0
        player.direct = 0
        player.frame = 0
        
    def maptoscreen(self,px,py): #checks what subsurface of the map fits on
        #the screen and converts the point(px,py) from world coordinates to
        #screen coordinates
        #mapx and mapy are the coords of the top left point of your screen
        #sx and sy are the converted (px,py) coords
        if px < 600:
            self.mapx = 0
            self.sx = px
        elif px > self.sizex - 600:
            self.mapx = self.sizex - 1200
            self.sx = 1200 - (self.sizex - px)
        else:
            self.mapx = px - 600
            self.sx = 600

        if py < 350:
            self.mapy = 0
            self.sy = py
        elif py > self.sizey - 350:
            self.mapy = self.sizey - 700
            self.sy = 700 - (self.sizey - py)
        else:
            self.mapy = py - 350
            self.sy = 350

class Player:
    def __init__(self,level,hp,mp,exp,atk,defence,crit,
                 image,x,y):
        self.level=level
        self.hp=hp
        self.tothp=hp
        self.mp=mp
        self.totmp=mp
        self.exp=exp
        self.atk=atk
        self.defence=defence
        self.crit=crit
        self.image=image
        self.x=x
        self.y=y
        self.direct=down #direction
        self.frame=0 #frame that you're in
        self.wid=self.image[0][0][0].get_width()//2
        self.hi=self.image[0][0][0].get_height()//2
        self.invincible=0 #counter for your invincibility after you're hit
        self.action=walk
        self.attacking=False #whether you're attacking or not
        self.AtkRect=Rect(0,0,0,0) #your attacking rect
        self.mpdelay=10 #delays mp regen
        
    def attack(self,Range): #Random number between a certain range to use as your attack
        return randint(self.atk-Range,self.atk+Range)
    
    def critical(self): #finds whether you hit a critical or not
        crits=[]
        for i in range(self.crit//5):
            crits.append(1)
        for i in range(20-self.crit//5):
            crits.append(0)
        if choice(crits)==1:
            return True
        return False
    
    def critatk(self,Range): #multiplies your attack if critical
        return int(randint(self.atk-Range,self.atk+Range)*1.5)
    
    def move(self):

        #all the actions are done here
        olddirect = self.direct
        oldx,oldy = self.x,self.y
        newaction=-1
        self.attacking=False
        if self.action in attacks: #these actions finish themselves even if you let go of the key
            newaction=self.action
        keys=key.get_pressed()
        if keys[K_UP]:
            self.direct = up
            newaction = walk
            self.y-=10
        elif keys[K_LEFT]:
            self.direct = left
            newaction = walk
            self.x-=10
        elif keys[K_DOWN]:
            self.direct = down
            newaction = walk
            self.y+=10
        elif keys[K_RIGHT]:
            self.direct = right
            newaction = walk
            self.x+=10
        elif keys[K_SPACE]:
            newaction = basic
        elif keys[K_v] and self.level>=8:
            newaction = ray
        elif keys[K_c] and self.level>=6:
            newaction = pierce
        elif keys[K_z] and self.level>=2:
            newaction = spin
        elif keys[K_LALT] or keys[K_RALT]:
            newaction = dash
        elif keys[K_x] and self.level>=4:
            newaction = slash
        elif keys[K_LCTRL] and self.level>=10 or keys[K_RCTRL] and self.level>=10:
            newaction = blast
        elif newaction not in attacks:
            self.frame=0
            self.action=0

        if self.action in attacks: #to make skills non interuptable
            newaction=self.action
            self.x,self.y=oldx,oldy
            self.direct=olddirect
       
        if newaction==self.action: #adds a frame if its the same skill
            self.frame+=delay[self.action]
            if self.frame>=len(self.image[self.direct][self.action]):
                self.frame=0
                if self.action in attacks: #changes back to walking 
                    self.action=0
                
        elif newaction!=-1: #changes to a new skill
            #if the cooldown of that skill is done and you have enough mp
            if curcooldown[newaction]<=0 and self.mp-mpcosts[newaction]>=0:
                self.action=newaction
                curcooldown[newaction]=cooldown[newaction]
                self.frame=0
                if self.action in attacks:
                    self.attacking=True #you are attacking

        if curlevel.check(self.x,self.y)==True: 
            self.x,self.y = oldx,oldy

    def cooldownup(self): #updates the cooldowns of your skills
        for i in range(len(curcooldown)):
            if curcooldown[i]>0:
                curcooldown[i]-=1
        
    def hit(self,monsteratk): #when an enemy hits you
        if monsteratk-self.defence<=0:
            self.hp-=1
            return 1
        self.hp-=monsteratk-self.defence
        return monsteratk-self.defence
    
    #draws hp,mp and exp bars
    def hpbar(self,x,y,l,w):
        loc=(x,y)
        loc2=(x+35,y+10)
        loc3=(x+35,y+8)
        loc4=(x+147,y+8)
        screen.blit(emptybarPic,loc)
        screen.blit(hpPic.subsurface(0,0,int(l*self.hp/self.tothp),w),loc2)
        screen.blit(blurlinePic,loc2)
        txt=arialFont.render("Hp",True,(255,255,255))
        screen.blit(txt,loc3)
        txt=arialFont.render(str(self.hp)+"/"+str(self.tothp),True,(255,255,255))
        screen.blit(txt,loc4)
        
    def mpbar(self,x,y,l,w):
        loc=(x,y)
        loc2=(x+35,y+10)
        loc3=(x+35,y+8)
        loc4=(x+147,y+8)
        screen.blit(emptybarPic,loc)
        screen.blit(mpPic.subsurface(0,0,int(l*self.mp/self.totmp),w),loc2)
        screen.blit(blurlinePic,loc2)
        txt=arialFont.render("Mp",True,(255,255,255))
        screen.blit(txt,loc3)
        txt=arialFont.render(str(self.mp)+"/"+str(self.totmp),True,(255,255,255))
        screen.blit(txt,loc4)
        
    def expbar(self,x,y,l,w):
        loc=(x,y)
        loc2=(x+35,y+10)
        loc3=(x+35,y+8)
        loc4=(x+147,y+8)
        screen.blit(emptybarPic,loc)
        screen.blit(expPic.subsurface(0,0,int(l*self.exp/self.totexp),w),loc2)
        screen.blit(blurlinePic,loc2)
        txt=arialFont.render("Exp",True,(255,255,255))
        screen.blit(txt,loc3)
        txt=arialFont.render(str(self.exp)+"/"+str(self.totexp),True,(255,255,255))
        screen.blit(txt,loc4)

    def Rectup(self):
        #updates your hitbox rects and if you are attacking, your attacking rects
        if self.action==0:
            self.rectwid=self.image[self.direct][0][int(self.frame)].get_width()//2
            self.recthi=self.image[self.direct][0][int(self.frame)].get_height()//2
        else:
            self.rectwid=self.image[0][0][0].get_width()//2
            self.recthi=self.image[0][0][0].get_height()//2
        self.Rect=Rect(self.x-self.rectwid,self.y-self.recthi,self.rectwid*2,self.recthi*2)
        #self.Rect=Rect(self.x-self.wid,self.y-self.hi,self.wid*2,self.hi*2)

        if self.attacking:
            #changes based on different offsets
            if self.action==basic:
                if self.direct == up:
                    self.AtkRect=Rect(self.x-self.wid,self.y-self.hi-30,self.wid*2,self.hi*2)
                elif self.direct == right:
                    self.AtkRect=Rect(self.x-self.wid+30,self.y-self.hi,self.wid*2,self.hi*2)
                elif self.direct == left:
                    self.AtkRect=Rect(self.x-self.wid-30,self.y-self.hi,self.wid*2,self.hi*2)
                elif self.direct == down:
                    self.AtkRect=Rect(self.x-self.wid,self.y-self.hi+30,self.wid*2,self.hi*2)
            elif self.action==ray:
                self.AtkRect=Rect(self.x-self.wid-50,self.y-self.hi-50,self.wid*2+100,self.hi*2+100)
            elif self.action==pierce:
                if self.direct==up:
                    self.AtkRect=Rect(self.x-self.wid,self.y-self.hi-185,self.wid*2,
                                      self.hi*2-50)
                elif self.direct == right:
                    self.AtkRect=Rect(self.x-self.wid+50+185,self.y-self.hi,self.wid*2-50,
                                      self.hi*2)
                elif self.direct == left:
                    self.AtkRect=Rect(self.x-self.wid-185,self.y-self.hi,self.wid*2-50,
                                      self.hi*2-50)
                elif self.direct == down:
                    self.AtkRect=Rect(self.x-self.wid,self.y-self.hi+185+50,self.wid*2,
                                      self.hi*2-50)
            elif self.action==spin:
                self.AtkRect=Rect(self.x-self.wid,self.y-self.hi,self.wid*2,self.hi*2)

            elif self.action==slash:
                if self.direct==up:
                    self.AtkRect=Rect(self.x-self.wid,self.y-self.hi-120,self.wid*2,
                                      self.hi*2-70)
                elif self.direct == right:
                    self.AtkRect=Rect(self.x-self.wid+120,self.y-self.hi,self.wid*2-70,
                                      self.hi*2)
                elif self.direct == left:
                    self.AtkRect=Rect(self.x-self.wid-120,self.y-self.hi,self.wid*2-70,
                                      self.hi*2)
                elif self.direct == down:
                    self.AtkRect=Rect(self.x-self.wid,self.y-self.hi+120,self.wid*2,
                                      self.hi*2-70)
            elif self.action==blast:
                if self.direct==up:
                    self.AtkRect=Rect(self.x-self.wid,self.y-self.hi-375,self.wid*2,
                                      self.hi*2-70)
                elif self.direct == right:
                    self.AtkRect=Rect(self.x-self.wid+375,self.y-self.hi,self.wid*2-70,
                                      self.hi*2)
                elif self.direct == left:
                    self.AtkRect=Rect(self.x-self.wid-375,self.y-self.hi,self.wid*2-70,
                                      self.hi*2)
                elif self.direct == down:
                    self.AtkRect=Rect(self.x-self.wid,self.y-self.hi+375,self.wid*2,
                                      self.hi*2-70)
    def dimup(self):#updates dimensions (length and width of the current image you are on)
        self.wid=self.image[self.direct][self.action][int(self.frame)].get_width()//2
        self.hi=self.image[self.direct][self.action][int(self.frame)].get_height()//2
        
    def knockback(self,monster): #knocking you back when hit by a monster
        oldx,oldy = self.x,self.y
        if monster.direct==monster.left:
            self.x-=20
        elif monster.direct==monster.right:
            self.x+=20
        elif monster.direct==monster.up:
            self.y-=20
        elif monster.direct==monster.down:
            self.y+=20
        elif monster.direct==monster.downleft:
            self.x-=20
            self.y+=10
        elif monster.direct==monster.downright:
            self.x+=20
            self.y+=10
        elif monster.direct==monster.upright:
            self.x+=20
            self.y-=10
        elif monster.direct==monster.upleft:
            self.x-=20
            self.y-=10
            
        if curlevel.check(self.x,self.y)==True:
            self.x,self.y = oldx,oldy
        
    def invincibleup(self): #updates invincibility counter
        if kirito.invincible>0:
            kirito.invincible-=1
    def mpup(self): #regens mp
        self.mpdelay-=1
        if self.totmp-self.mp>=1 and self.mpdelay<=0:
            self.mp+=1
            self.mpdelay=10
    def loadexp(self): #loads the text file telling you how much exp you need to advance
        #each level
        infile = open("exp.txt","r")
        exp = infile.read().strip().split()
        self.levels = [i.split('-')[0] for i in exp]
        self.exps = [i.split('-')[1] for i in exp]
        infile.close()
        self.totexp=int(self.exps[self.level-1])
    def levelcheck(self): #checks if you leveled up
        if self.exp>=self.totexp:
            self.levelup()
    def levelup(self): #updates your stats when you level up
        self.level+=1
        self.exp-=self.totexp
        self.totexp=int(self.exps[self.level-1])
        self.atk+=5
        self.defence+=5
        self.tothp+=50
        self.hp=self.tothp
        self.totmp+=10
        self.mp=self.totmp
        if self.level>=11:
            mpcosts[dash]=3
        if self.level>=13:
            mpcosts[spin]=7
        if self.level>=16:
            mpcosts[slash]=15
            mpcosts[pierce]=20
        if self.level>=18:
            mpcosts[ray]=75
        if self.level>=20:
            mpcosts[blast]=1
            cooldown[blast]=10
    def checkdie(self): #goes back to your saved stats when you die
        if self.hp<=0:
            self.level = curlevel.savelevel
            self.exp = curlevel.saveexp
            self.tothp = curlevel.savehp
            self.totmp = curlevel.savemp
            self.hp = self.tothp
            self.mp = self.totmp
            self.atk = curlevel.saveatk
            self.defence = curlevel.savedefence
            curlevel.stage = curlevel.savestage
            curlevel.mapnum = curlevel.savemapnum
            curlevel.load(curlevel.mapnum)
            del alive[:]
            del dmgs[:]
            del dmgposx[:]
            del dmgposy[:]
            del dmgmapx[:]
            del dmgmapy[:]
            del dmgtimes[:]
            del dmgalpha[:]
            del dmgpic[:]
            self.x,self.y = curlevel.savex,curlevel.savey
            curlevel.maptoscreen(self.x,self.y)
            storyparts(1,13)
        
class Enemy:
    def __init__(self,hp,exp,level,atk,defence,drops,image,x,y,
                 sprite,speed,Range,sight,sightspeed,Type,framelimit):
        self.hp=hp
        self.tothp=hp
        self.exp=exp
        self.level=level
        self.atk=atk
        self.defence=defence
        self.drops=drops
        self.image=image
        self.x=x
        self.y=y
        self.direct=0
        self.frame=0
        self.sprite=sprite #list of the 
        #indices for the directions (i didn't want to make them global variables
        #since they changes based on monsters)
        self.down = sprite[0]
        self.left = sprite[1]
        self.right = sprite[2]
        self.up = sprite[3]
        self.downleft = sprite[4]
        self.downright = sprite[5]
        self.upright = sprite[6]
        self.upleft = sprite[7]
        self.delay=0
        self.normspeed=speed 
        self.sightspeed=sightspeed
        self.speed=speed
        self.hpx=self.image[0][0].get_width()
        self.hpy=self.image[0][0].get_height()
        self.Range=Range
        self.sight=sight
        self.wid=self.image[self.direct][int(self.frame)].get_width()//2
        self.hi=self.image[self.direct][int(self.frame)].get_height()//2
        self.Rect=Rect(self.x-self.wid,self.y-self.hi,self.wid*2,self.hi*2)
        self.type=Type
        self.skilltime=250
        self.framelimit=framelimit
        
    def bossskills(self): #special skills the bosses use
        self.skilltime-=1
        if self.type=="boss1" and self.skilltime<=0:
            #spawns 3 monsters
            monster=curlevel.monsters[2].copy()
            monster.x,monster.y=570,1150
            alive.append(monster)
            
            monster=curlevel.monsters[2].copy()
            monster.x,monster.y=1025,1150
            alive.append(monster)
            
            monster=curlevel.monsters[2].copy()
            monster.x,monster.y=800,1580
            alive.append(monster)
            
            self.skilltime=250

        if self.type=="boss2" and self.skilltime<=0:
            #teleports to a random location
            self.x,self.y = choice([(325,745),(1333,685),(1300,1400),(300,1450)])

            self.skilltime=250

        if self.type=="boss3" and self.skilltime<=0:
            #spawns 2 monsters
            monster=curlevel.monsters[2].copy()
            monster.x,monster.y=720,1250
            alive.append(monster)
            
            monster=curlevel.monsters[2].copy()
            monster.x,monster.y=720,400
            alive.append(monster)
            
            self.skilltime=250
        
    def randmove(self): #random movement
        oldx,oldy = self.x,self.y
        olddirect=self.direct
        choices=[1,2,3,4]
        if self.direct==self.right:
            for i in range(8):
                choices.append(1)
        if self.direct==self.left:
            for i in range(8):
                choices.append(2)
        if self.direct==self.down:
            for i in range(8):
                choices.append(3)
        if self.direct==self.up:
            for i in range(8):
                choices.append(4)
                
        choose=choice(choices)
        
        if choose==1:
            self.x+=5
            self.direct=self.right
        elif choose==2:
            self.x-=5
            self.direct=self.left
        elif choose==3:
            self.y+=5
            self.direct=self.down
        elif choose==4:
            self.y-=5
            self.direct=self.up

        if self.x>curlevel.sizex or self.x<0 or self.y>curlevel.sizey or self.y<0:
            self.x,self.y = oldx,oldy
            
        elif curlevel.check(self.x,self.y) == True:
            self.x,self.y = oldx,oldy
            
    def move(self,X,Y): #monster chases you
        #the monster goes diagonally until it lines up with you either
        #horizontaly or vertically then it goes up,down,left, or right
        oldx,oldy = self.x,self.y
        x, y = self.x, self.y
        deltax = X - x
        deltay = Y - y
        olddirect=self.direct
        if abs(deltax)<5:
            if deltay>0:
                self.direct=self.down
                self.y+=5
            else:
                self.direct=self.up
                self.y-=5
        elif abs(deltay)<5:
            if deltax>0:
                self.direct=self.right
                self.x+=5
            else:
                self.direct=self.left
                self.x-=5
        elif deltax>0 and deltay>0:
            self.direct=self.downright
            self.x+=5
            self.y+=5
        elif deltax>0 and deltay<0:
            self.direct=self.upright
            self.x+=5
            self.y-=5
        elif deltax<0 and deltay>0:
            self.direct=self.downleft
            self.x-=5
            self.y+=5
        elif deltax<0 and deltay<0:
            self.direct=self.upleft
            self.x-=5
            self.y-=5

        if self.x>curlevel.sizex or self.x<0 or self.y>curlevel.sizey or self.y<0:
            self.x,self.y = oldx,oldy

        elif curlevel.check(self.x,self.y) == True:
            self.x,self.y = oldx,oldy                    

    def attack(self): #returns the amount you hit
        return randint(self.atk-self.Range,self.atk+self.Range)
    
    def detect(self,X,Y): #if the monster detects you, it chases you
        #checks if you are within the circle of its sight
        if hypot(X-self.x,Y-self.y)<=self.sight:
            self.speed=self.sightspeed
            return True
        self.speed=self.normspeed
        return False
    
    def hit(self,playeratk): #when the monster is hit by the player
        if playeratk-self.defence<=0:
            self.hp-=1
            return 1
        self.hp-=playeratk-self.defence
        return playeratk-self.defence
    
    def hpbar(self,mapx,mapy): #draws hp bar
        draw.rect(screen,(255,0,0),(self.x-self.hpx//2-mapx,self.y-self.hpy//2-mapy,
                                    self.hpx*self.hp//self.tothp,5))
        draw.rect(screen,(0,0,0),(self.x-self.hpx//2-mapx,self.y-self.hpy//2-mapy,
                                  self.hpx,5),1)       
        
        
    def frameup(self): #updates the frame every self.delay frames
        self.delay-=1
        if self.delay==0:
            self.frame+=1
            if self.frame>=self.framelimit:
                self.frame=0
        if self.delay<=-1:
            self.delay=self.speed
        
        

    def Rectup(self): #updates the hitbox
        self.wid=self.image[self.direct][int(self.frame)].get_width()//2
        self.hi=self.image[self.direct][int(self.frame)].get_height()//2
        self.Rect=Rect(self.x-self.wid,self.y-self.hi,self.wid*2,self.hi*2)

    def copy(self): #returns a copy of itself
        return Enemy(self.hp,self.exp,self.level,self.atk,self.defence,
                     self.drops,self.image,self.x,self.y,self.sprite,
                     self.speed,self.Range,self.sight,self.sightspeed,self.type,
                     self.framelimit)
        

def showdmg(dmg,x,y,nums,a): #blits the damage numbers on the screen
    dmg=str(dmg)
    wid=nums[0].get_width()
    count=0
    for num in dmg:
        screen.blit(nums[int(num)],(x+count*wid,y))
        count+=1

def updmg(): #decreases the y value of the damage numbers
    if len(dmgs)>0:
        for i in range(len(dmgs)):
            dmgmapx[i]=dmgposx[i]-curlevel.mapx
            dmgmapy[i]=dmgposy[i]-curlevel.mapy
            showdmg(dmgs[i],dmgmapx[i],int(dmgmapy[i]),dmgpic[i],dmgalpha[i])
            dmgposy[i]-=1
            dmgtimes[i]-=1
            dmgalpha[i]-=2

def killdmg(): #removes the damage numbers from the lists once they're finished
    killlist=[]
    for i in range(len(dmgs)):
        if dmgtimes[i]<0:
            killlist.append(i)
    killlist.sort(reverse=True)

    if len(killlist)>0:
        for i in killlist:
            del dmgs[i]
            del dmgposx[i]
            del dmgposy[i]
            del dmgmapx[i]
            del dmgmapy[i]
            del dmgtimes[i]
            del dmgalpha[i]
            del dmgpic[i]

def update(objects): #updates the monsters' frames abd hitboxes
    for name in objects:
        name.frameup()
        name.Rectup()

def monstermove(monsters): #moves all the alive monsters
    for i in range(len(monsters)):
        if monsters[i].delay==0:
            if monsters[i].detect(kirito.x,kirito.y)==True:
                monsters[i].move(kirito.x,kirito.y)
            else:
                monsters[i].randmove()
                

def monsterattack(monsters,player): #the monsters attack
    for i in range(len(monsters)):
        #checks if they hit your hitbox
        if monsters[i].Rect.colliderect(player.Rect) and player.invincible==0:
            dmg=player.hit(monsters[i].attack())
            player.knockback(monsters[i])
            player.invincible=25
            dmgx=player.x-player.image[0][0][0].get_width()//2
            dmgy=player.y-player.image[0][0][0].get_height()//2-24
            dmgs.append(dmg)
            dmgposx.append(dmgx)
            dmgposy.append(dmgy)
            dmgmapx.append(0)
            dmgmapy.append(0)
            dmgtimes.append(50)
            dmgalpha.append(255)
            dmgpic.append(nums)


def playerattack(monsters,player,Range): #player attacks
    #lowers your mana
    player.mp-=mpcosts[player.action]
    #ray and dash have seperate effects that happen here
    if player.action==ray:
        gainedhp=player.tothp//10
        if player.hp+gainedhp>player.tothp:
            gainedhp=player.tothp-player.hp
        player.hp+=gainedhp
    if player.action==dash:
        oldx,oldy=player.x,player.y
        if player.level>=11:
            if player.direct==right:
                player.x+=150
            elif player.direct==left:
                player.x-=150
            elif player.direct==up:
                player.y-=150
            elif player.direct==down:
                player.y+=150
        else:
            if player.direct==right:
                player.x+=100
            elif player.direct==left:
                player.x-=100
            elif player.direct==up:
                player.y-=100
            elif player.direct==down:
                player.y+=100

        try:
            if curlevel.check(player.x,player.y)==True:
                player.x,player.y = oldx,oldy
        except:
            player.x,player.y = oldx,oldy
        
    for monster in monsters:
        if monster.Rect.colliderect(player.AtkRect): #checks if your attack rect
            #hits their hitbox

            #num is the number of attacks
            #mult is the damage multiplier of each skill
            if player.action==basic:
                num=1
                mult=1
            elif player.action==ray:
                if player.level>=18:
                    num=5
                    mult=3.5
                else:
                    num=3
                    mult=2.5
            elif player.action==pierce:
                if player.level>=16:
                    num=2
                    mul=7.5
                else:
                    num=2
                    mult=4
            elif player.action==spin:
                if player.level>=13:
                    num=3
                    mult=2.5
                else:
                    num=2
                    mult=1.5
            elif player.action==slash:
                if player.level>=16:
                    num=4
                    mult=4
                else:
                    num=2
                    mult=2
            elif player.action==blast:
                if player.level>=20:
                    num=10
                    mult=15
                else:
                    num=5
                    mult=10
            dodmg(monster,player,num,mult,Range)
    player.AtkRect=Rect(0,0,0,0)#deletes your attack rect so you'd have to
    #cast the skill again to hit the monster
    monsterkill() #checks if monsters died

def dodmg(monster,player,atknum,mult,Range): #calculates the damage
    for i in range(atknum): #how many hits the skill does
        if player.critical():
            dmgs.append(monster.hit(int(player.critatk(Range)*mult)))#multiplies by the damage multiplier of that skill
            dmgpic.append(nums2)
        else:
            dmgs.append(monster.hit(int(player.attack(Range)*mult)))
            dmgpic.append(nums3)
        dmgposx.append(monster.x-monster.wid+randint(-5,5))
        dmgposy.append(monster.y-monster.hi-24-(27*i))
        dmgmapx.append(0)
        dmgmapy.append(0)
        dmgtimes.append(50)
        dmgalpha.append(255)

def monsterdraw(monsters): #draws all the monsters
    for i in range(len(monsters)):
        monsters[i].imove(screen)
        monsters[i].hpbar()

def monsterkill(): #deletes monsters that have no hp 
    killlist=[]
    for monster in alive:
        if monster.hp<=0:
            killlist.append(alive.index(monster))
            kirito.exp+=monster.exp
            kirito.levelcheck()
            if kirito.exp>kirito.totexp:
                for i in range(20):
                    kirito.levelcheck()
    killlist.sort(reverse=True)

    if len(killlist)>0:
        for i in killlist:
            del alive[i]

def spawnmonsters(): #spawns monsters
    if monstercount<curlevel.limit and spawndelay==0: #if the map has not reached its spawn limit
        if len(curlevel.spawnloc)>0:
            Mons=[]#stores all the monsters who spawn in this map
            for i in range(len(curlevel.monsters)):
                if str(curlevel.mapnum) in curlevel.spawnmaps[i]:
                    Mons.append(curlevel.monsters[i])
            if len(Mons)>0:
                chlist=[]
                for i in range(len(Mons)):
                    chlist.append(i+1)
                num=choice(chlist) #chooses one of the monsters in Mons
                locx,locy=choice(curlevel.spawnloc) #chooses a random spawn location
                for i in range(len(Mons)):
                    if num==i+1:
                        monster=Mons[i].copy() #takes a copy of the instance so that
                        #the original instance stays unchanged 
                monster.x,monster.y=locx,locy #changes the monster's position to
                #the chosen spawn location
                alive.append(monster) #appends that monster to alive
    #special cases for spawning bosses
    if curlevel.stage=="" and curlevel.mapnum=="12" and len(alive)==0:
        monster=curlevel.monsters[3].copy()
        monster.x,monster.y=795,700
        alive.append(monster)
        alpha=0
        #blits some boss information before the room is drawn
        for i in range(255):
            screen.fill((0,0,0))
            bossinfo1.set_alpha(alpha)
            alpha+=1
            screen.blit(bossinfo1,(500,200))
            display.flip()

    if curlevel.stage=="2" and curlevel.mapnum=="12" and len(alive)==0:
        monster=curlevel.monsters[0].copy()
        monster.x,monster.y=325,745
        alive.append(monster)
        alpha=0
        for i in range(255):
            screen.fill((0,0,0))
            bossinfo2.set_alpha(alpha)
            alpha+=1
            screen.blit(bossinfo2,(500,200))
            display.flip()
        alpha=0
        for i in range(255):
            screen.fill((0,0,0))
            bossinfo3.set_alpha(alpha)
            alpha+=1
            screen.blit(bossinfo3,(500,200))
            display.flip()
        time.wait(2000)

    if curlevel.stage=="3" and curlevel.mapnum=="13" and len(alive)==0:
        monster=curlevel.monsters[3].copy()
        monster.x,monster.y=720,500
        alive.append(monster)
        alpha=0
        for i in range(255):
            screen.fill((0,0,0))
            bossinfo4.set_alpha(alpha)
            alpha+=1
            screen.blit(bossinfo4,(500,200))
            display.flip()
        alpha=0
        for i in range(255):
            screen.fill((0,0,0))
            bossinfo5.set_alpha(alpha)
            alpha+=1
            screen.blit(bossinfo5,(500,200))
            display.flip()
        time.wait(2000)
        

def drawicons(player): #draws all the skill icons seen in the info panel
    if player.level>=1:
        if skillRects[0].collidepoint(mx,my):
            screen.blit(skills3[0],(661,706))
        else:
            screen.blit(skills[0],(661,706))
        if player.level>=11:
            draw.rect(screen,(192,1,2),(660,706,31,31),1)
        else:
            draw.rect(screen,(0,0,255),(660,706,31,31),1)
        
    if player.level>=2:
        if skillRects[1].collidepoint(mx,my):
            screen.blit(skills3[1],(697,706))
        else:
            screen.blit(skills[1],(697,706))
        if player.level>=13:
            draw.rect(screen,(192,1,2),(697,706,31,31),1)
        else:
            draw.rect(screen,(0,0,255),(697,706,31,31),1)
    else:
        if skillRects[1].collidepoint(mx,my):
            screen.blit(skills4[1],(697,706))
        else:
            screen.blit(skills2[1],(697,706))
        
    if player.level>=4:
        if skillRects[2].collidepoint(mx,my):
            screen.blit(skills3[2],(732,706))
        else:
            screen.blit(skills[2],(732,706))
        if player.level>=16:
            draw.rect(screen,(192,1,2),(732,706,31,31),1)
        else:
            draw.rect(screen,(0,0,255),(732,706,31,31),1)
    else:
        if skillRects[2].collidepoint(mx,my):
            screen.blit(skills4[2],(732,706))
        else:
            screen.blit(skills2[2],(732,706))
        
    if player.level>=6:
        if skillRects[3].collidepoint(mx,my):
            screen.blit(skills3[3],(766,706))
        else:
            screen.blit(skills[3],(766,706))
        if player.level>=16:
            draw.rect(screen,(192,1,2),(766,706,31,31),1)
        else:
            draw.rect(screen,(0,0,255),(766,706,31,31),1)
    else:
        if skillRects[3].collidepoint(mx,my):
            screen.blit(skills4[3],(766,706))
        else:
            screen.blit(skills2[3],(766,706))
        
    if player.level>=8:
        if skillRects[4].collidepoint(mx,my):
            screen.blit(skills3[4],(810,706))
        else:
            screen.blit(skills[4],(810,706))
        if player.level>=18:
            draw.rect(screen,(192,1,2),(810,706,31,31),1)
        else:
            draw.rect(screen,(0,0,255),(810,706,31,31),1)
    else:
        if skillRects[4].collidepoint(mx,my):
            screen.blit(skills4[4],(810,706))
        else:
            screen.blit(skills2[4],(810,706))
        
    if player.level>=10:
        if skillRects[5].collidepoint(mx,my):
            screen.blit(skills3[5],(846,706))
        else:
            screen.blit(skills[5],(846,706))
        if player.level>=20:
            draw.rect(screen,(192,1,2),(846,706,31,31),1)
        else:
            draw.rect(screen,(0,0,255),(846,706,31,31),1)
    else:
        if skillRects[5].collidepoint(mx,my):
            screen.blit(skills4[5],(846,706))
        else:
            screen.blit(skills2[5],(846,706))

    for i in range(len(skillRects)):
        if skillRects[i].collidepoint(mx,my):
            screen.blit(skillinfos[i],(mx,my-150))

def loadsheet2(pic,frames,length): #loads monster pictures into a list of lists
    List1=[] 
    List2=[]
    List3=[]
    List4=[]
    List=[List1,List2,List3,List4] #one list for every direction

    for x in range(frames): #how many frames there are
        for y in range(length): #length of each frame
            List[x].append(image.load("%s%s%03d.png" %('monsters/',pic,x*length+y+1)))
            #print("%s%s%03d.png" %('monsters/',pic,y+1))
    return List
        

def loadlist(folder,name,start,end): #loads a list of pictures
    move=[]
    for i in range(start,end+1):
        move.append(image.load("%s/%s%d.png" % (folder,name,i)))
        
    return move
def loadlist2(folder,name,start,end): #loads a list of pictures ending with
    #3 digits (for your split program)
    move=[]
    for i in range(start,end+1):
        move.append(image.load("%s/%s%03d.png" % (folder,name,i)))
        
    return move


def makeStory(file,name,start,end): #variation of load list used to load the story pictures
    ''' This returns a list of pictures. They must be in the folder "name"
        and start with the name "name".
        start, end - The range of picture numbers 
    '''
    move = []
    for i in range(start,end+1):
        move.append(transform.smoothscale(image.load("%s/%s%d.png" % (file,name,i)), screen.get_size()))
        
    return move

def premenu(): #loop with the premenu screen
    running = True
    while running:
        for evt in event.get():
            if evt.type == QUIT:
                exit()
            if evt.type == KEYDOWN:
                if evt.key == K_KP_ENTER or evt.key == K_RETURN:
                    running = False

        screen.blit(screens[0],(0,0))
        display.flip()

def mainmenu(): #mainmenu screen
    running = True
    buttonRects=[Rect(535,450,155,65),Rect(465,535,285,45),
                     Rect(540,590,140,40),Rect(525,640,160,45)]
    button = 1
    while running:
        for evt in event.get():
            if evt.type == QUIT:
                exit()
            if evt.type == KEYDOWN:
                if evt.key == K_UP:
                    button-=1
                    if button<1:
                        button=4
                if evt.key == K_DOWN:
                    button+=1
                    if button>4:
                        button=1
                if evt.key == K_KP_ENTER or evt.key == K_RETURN:
                    running = False

        mx,my=mouse.get_pos()
        mb=mouse.get_pressed()
        
        for i in range(4):
            if buttonRects[i].collidepoint(mx,my):
                button=i+1
                if mb[0]==1:
                    running = False
        
        for i in range(4):
            if button==i+1:
                screen.blit(screens[i+1],(0,0))

        display.flip()
    #returns different destinations depending on which button you pressed
    if button == 1:
        return "play"
    elif button == 2:
        return "instructions"
    elif button == 3:
        return "story"
    elif button == 4:
        return "credits"

def instructions(): #instructions screen
    running = True
    closeRect = Rect(10,10,55,65)
    nextRect = Rect(1060,15,120,120)
    page = 1
    while running:
        click = False
        for evt in event.get():
            if evt.type == QUIT:
                exit()
            if evt.type == MOUSEBUTTONDOWN:
                click = True

        mx,my=mouse.get_pos()
        mb=mouse.get_pressed()

        if closeRect.collidepoint(mx,my) and mb[0]==1:
            running = False

        if nextRect.collidepoint(mx,my) and click:
            if page == 1:
                page = 2
            elif page == 2:
                page = 1
        if page == 1:
            screen.blit(screens[5],(0,0))
        elif page ==2 :
            screen.blit(screens[19],(0,0))
        display.flip()
    #goes back to the mainmenu when you're done
    return "mainmenu"

def Credits(): #credits screen
    running = True
    closeRect = Rect(15,15,55,65)
    while running:
        for evt in event.get():
            if evt.type == QUIT:
                exit()

        mx,my=mouse.get_pos()
        mb=mouse.get_pressed()

        if closeRect.collidepoint(mx,my) and mb[0]==1:
            running = False

        screen.blit(screens[6],(0,0))
        display.flip()
    return "mainmenu"

def story(): #story screens
    running = True
    page = 1
    closeRect = Rect(0,10,55,65)
    while running:
        for evt in event.get():
            if evt.type == QUIT:
                exit()
            if evt.type == KEYDOWN:
                #scroll through the stories with the arrow keys
                if evt.key == K_LEFT:
                    page-=1
                    if page<1:
                        page=1
                if evt.key == K_RIGHT:
                    page+=1
                    if page>12:
                        page=12
       
        mx,my=mouse.get_pos()
        mb=mouse.get_pressed()

        if closeRect.collidepoint(mx,my) and mb[0]==1:
            running = False

        screen.blit(screens[page+6],(0,0))
        display.flip()
    return "mainmenu"

def storyparts(pages,start): #displayes parts of the story throughout the actual game
    running = True
    page = start
    alpha = 1 
    alpha2 = 255
    while running:
        for evt in event.get():
            if evt.type == QUIT:
                exit()
            if evt.type == KEYDOWN:
                if evt.key == K_LEFT:
                    page-=1
                    if page<start:
                        page=start
                if evt.key == K_RIGHT:
                    page+=1
                    if page>start+pages-1:
                        page=start+pages-1
                        running = False
                        
        if page==start: #fades in the first screen
            stories[page].set_alpha(alpha)
            alpha+=1
            if alpha>255:
                alpha=255
            
        screen.blit(stories[page],(0,0))
        
        display.flip()
        
    for i in range(51): #fades out the last screen
        screen.fill((0,0,0))
        stories[page].set_alpha(alpha2)
        alpha2-=5
        screen.blit(stories[page],(0,0))
        display.flip()
    
def menu(): #keeps track of where you are during the menu
    page = "mainmenu"
    while page != "play": #if page is play, start the game
        if page == "mainmenu":
            page = mainmenu()
        if page == "instructions":
            page = instructions()
        if page == "story":
            page = story()
        if page == "credits":
            page = Credits()


screens=makeStory("menu pic","s",1,20) #load the menu screens
stories=makeStory("menu pic","",1,14) #load the story screens

#loads boss info pictures
bossinfo1=image.load("info/boss1.png")
bossinfo2=image.load("info/boss2.png")
bossinfo3=image.load("info/boss2.1.png")
bossinfo4=image.load("info/boss3.png")
bossinfo5=image.load("info/boss3.1.png")

#loads pictures needed for the hp,mp and exp bars
emptybarPic=image.load("bars/emptybar4.png")
blurlinePic=image.load("bars/blurline4.png")
mpPic=image.load("bars/mpfit4.png")
hpPic=image.load("bars/hpfit4.png")
expPic=image.load("bars/expfit4.png")

#loads pictures for info panel
khead=image.load("info/kirito.png")
mapinfo=image.load("info/map1.1.png")

skills=loadlist("info","4.",1,6)
skills2=loadlist("info","1.",1,6)
skills3=loadlist("info","2.",1,6)
skills4=loadlist("info","3.",1,6)
skillRects=[Rect(661,706,30,30),Rect(697,706,30,30),Rect(732,706,30,30),
            Rect(766,706,30,30),Rect(810,706,30,30),Rect(846,706,30,30)]
skillinfos=loadlist("info","d",1,6)
   
#skills for kirito
moves=[]
rights=[]
lefts=[]
downs=[]
ups=[]

#appends skills to respective direction
downs.append(loadlist("move","character",1,3))
lefts.append(loadlist("move","character",4,6))
rights.append(loadlist("move","character",7,9))
ups.append(loadlist("move","character",10,12))
downs.append(loadlist("basicattack1","basic1.",0,4))
lefts.append(loadlist("basicattack1","basic1.",5,9))
rights.append(loadlist("basicattack1","basic1.",10,14))
ups.append(loadlist("basicattack1","basic1.",15,19))
downs.append(loadlist("shiningray","ray1.",1,9))
lefts.append(loadlist("shiningray","ray2.",1,9))
rights.append(loadlist("shiningray","ray3.",1,9))
ups.append(loadlist("shiningray","ray4.",1,9))
downs.append(loadlist("pierce","p5.",1,6))
lefts.append(loadlist("pierce","p4.",1,6))
rights.append(loadlist("pierce","p3.",1,6))
ups.append(loadlist("pierce","p6.",1,6))
downs.append(loadlist("spin","spin",1,5))
lefts.append(loadlist("spin","spin3.",1,5))
rights.append(loadlist("spin","spin1.",1,5))
ups.append(loadlist("spin","spin2.",1,5))
downs.append(loadlist("dash","d3.",1,6))
lefts.append(loadlist("dash","d1.",1,6))
rights.append(loadlist("dash","d",1,6))
ups.append(loadlist("dash","d2.",1,6))
downs.append(loadlist("slash","slash3.",1,5))
lefts.append(loadlist("slash","slash1.",1,5))
rights.append(loadlist("slash","slash",1,5))
ups.append(loadlist("slash","slash2.",1,5))
downs.append(loadlist("blast2","b4.",1,8))
lefts.append(loadlist("blast2","b1.",1,8))
rights.append(loadlist("blast2","b2.",1,8))
ups.append(loadlist("blast2","b3.",1,8))

#appends directions to another list to make a 3-D list
moves.append(downs)
moves.append(lefts)
moves.append(rights)
moves.append(ups)

#loads damge number images
nums=(loadlist2("dmg","dmg3",0,9))
nums2=(loadlist2("dmg","dmg1",0,9))
nums3=(loadlist2("dmg","dmg2",0,9))

#assigns indices to actions the player does
down=0
left=1
right=2
up=3
walk=0
basic=1
ray=2
pierce=3
spin=4
dash=5
slash=6
blast=7

attacks=[basic,ray,pierce,spin,dash,slash,blast]#the attacks
delay=[0.5,0.6,0.5,0.4,0.5,0.75,0.5,0.5]#delay for each action
curcooldown=[0 for i in range(8)] #current cooldown
cooldown=[0,10,10,10,10,0,10,250] #cooldown duration in frames
mpcosts=[0,0,100,25,10,5,20,42] 

#lists for the damage numbers
dmgs=[]
dmgposx=[]
dmgposy=[]
dmgmapx=[]
dmgmapy=[]
dmgtimes=[]
dmgalpha=[]
dmgpic=[]

#Sir, if you want to skip a stage or give kirito OP attack, this is where you do it
#to skip the ice maze make curlevel = MAP("3","9")
curlevel = MAP("","10") #creates the instance of the map you are in(stage,map)
kirito=Player(1,500,100,0,20,30,10,moves,300,400) #creates the player

alive=[]#list of all monsters in the map
spawndelay=100 #spawns monsters every 100 frames
poisondelay=100 #delay for poison in one of the boss rooms
stundelay=500 #delay for stun in one of the boss rooms
deathRect=Rect(1275,655,35,65) #automatic death in last stage

#loads neccesary things
curlevel.maptoscreen(kirito.x,kirito.y) 
kirito.loadexp() 
curlevel.loadmonsters()

#menu and begin the game
premenu()
menu()
storyparts(4,0)

running = True
myClock = time.Clock()
while running:
    for evnt in event.get():               
        if evnt.type == QUIT:
            running = False
        if evnt.type == KEYDOWN:
            if evnt.key == K_ESCAPE:
                running = False

    screen.fill((0,0,0))
    
    mx,my=mouse.get_pos()
    mb=mouse.get_pressed()

    #updates kirito
    kirito.cooldownup()
    kirito.invincibleup()
    kirito.mpup()

    #spawns monsters
    monstercount=len(alive)

    spawndelay-=1
    if spawndelay<0:
        spawndelay=100
    spawnmonsters()

    #moves kirito and monsters and updates both
    monstermove(alive)
    update(alive)
    if stundelay>=0:
        kirito.move()
    kirito.dimup()
    kirito.Rectup()
    curlevel.maptoscreen(kirito.x,kirito.y)

    #monster attacjs
    monsterattack(alive,kirito)

    #special attacks for bosses
    if curlevel.stage=="" and curlevel.mapnum=="12":
        for monster in alive:
            monster.bossskills()

    elif curlevel.stage=="2" and curlevel.mapnum=="12" :
        poisondelay-=1
        if poisondelay == 0:
            kirito.hp-=25
            poisondelay=100
        for monster in alive:
            monster.bossskills()

    elif curlevel.stage=="3" and curlevel.mapnum=="13" :
        stundelay-=1
        if stundelay<-50:
            stundelay=500
        for monster in alive:
            monster.bossskills()    

    #kirito attacks   
    if kirito.attacking:
        playerattack(alive,kirito,5)

    #checks if kirito died
    kirito.checkdie()

    #transfers you to the next dungeon after you beat a boss
    if curlevel.stage=="" and curlevel.mapnum=="12" :
        if len(alive)==0:
            curlevel.bosstransfer(kirito)
    elif curlevel.stage=="2" and curlevel.mapnum=="12" :
        if len(alive)==0:
            curlevel.bosstransfer(kirito)
    elif curlevel.stage=="3" and curlevel.mapnum=="13" :
        if len(alive)==0:
            curlevel.bosstransfer(kirito)
    elif curlevel.stage=="4":
        if deathRect.collidepoint(kirito.x,kirito.y):
            kirito.hp=0
            storyparts(3,10)
            quit()
    else:#otherwise checks for portals
        curlevel.portalcheck(kirito)
    #checks if you're at a save crystal
    curlevel.savecheck(kirito)
    #draws everything
    curlevel.draw(kirito,alive)

    #deletes old damage and updates new ones
    killdmg()
    updmg()
        
    myClock.tick(25)
    
    display.flip()
    
quit()
