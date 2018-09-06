#Gerekli modüller eklendi
import pygame, sys, time, random
from pygame.locals import *

#Pencere boyutu ve renklerin ayarları yapıldı
pencereGenis = 800
pencereYuksek = 600
Siyah = (0, 0, 0)
Beyaz = (255, 255, 255)

#Çıkış fonksiyonu tanımlandı
def cikis():
        pygame.quit()
        sys.exit()

#Ekrana yazdıracağımız Hız için fonksiyon tanımı yapıldı
def yaziYaz(yazi, tip, yuzey, x, y):
        yaziS = tip.render(yazi, 1, Beyaz)
        yaziRect = yaziS.get_rect()
        yaziRect.topleft = (x, y)
        yuzey.blit(yaziS, yaziRect)


def carpisma(arabaBirRect, arabaIkiRect):
        if arabaBirRect.colliderect(arabaIkiRect):
                return True
        else:
                return False


pygame.init()

saat = pygame.time.Clock()

pencereYuzeyi = pygame.display.set_mode((pencereGenis, pencereYuksek), 0, 32)
pygame.display.set_caption('Asama3 - Gelismis araba Oyunu')

tip = pygame.font.SysFont(None, 48)

araba = pygame.Rect(400, 450, 60, 100)
solBariyer = pygame.Rect(0, 0, 10, 1000)
sagBariyer = pygame.Rect(650, 0, 10, 1000)

#Birbirlerine rakip olacak arabaları ekliyoruz
arabaResim = pygame.image.load('araba.gif')
araba1Resim = pygame.image.load('araba1.gif')
araba2Resim = pygame.image.load('araba2.gif')
araba3Resim = pygame.image.load('araba3.gif')
yol = pygame.Rect(100, 0, 800, 1000)
yolResim = pygame.image.load('yol.jpg')
bariyer = pygame.image.load('bariyer.jpg')

gitSola = False
gitSaga = False
gitYukari = False
gitAsagi = False
Hizlan = False
Yavasla = False
YolDisi = False


arabaBelir = False #Kırmızı arabalar için olan sayaç artırılacağı zaman True olacak
sariArabaBelir = False #Sarı arabalar için olan sayaç artırılacağı zaman True olacak
elFreni = False
#kirmizi rakip = rakip

#Arabaların renklerine göre sayaçlar belirlendi
rakipSayac = 0
sariRakip = 200
rakip = 100
sariRakipSayac = 0
beyazRakip = 500
beyazRakipSayac = 0

#Yeni araba ekleyip, eksilenleri silebileceğimiz bir dizi oluşturuyoruz("arabalar=[]")
arabalar = []
sariArabalar = []
beyazArabalar = []


Hiz = 0.0

while True:

        for olay in pygame.event.get():
               if olay.type == QUIT:
                  pygame.quit()
                  sys.exit()
               if olay.type == KEYDOWN:
                  if olay.key == K_LEFT:
                     gitSaga = False
                     gitSola = True
                  if olay.key == K_RIGHT:
                     gitSola = False
                     gitSaga = True
                #Klavyede sağ ok tuşuna basıldığında Kırmızı arabalar için sayaç çalıştırılacak
                     arabaBelir = True

                  if olay.key == K_UP:
                     elFreni = False
                     Yavasla = False
                     gitYukari = True
                     gitAsagi = False
                     Hizlan = True
                #Klavyede yukarı ok tuşuna basılırsa Sarı arabaların sayacı çalıştırılacak
                     sariArabaBelir = True

                  if olay.key == K_DOWN:
                     if Hiz > 0:
                       Yavasla = False
                       elFreni = True
                       Hizlan = False
                     else:
                       gitAsagi = True
                  if olay.key == K_SPACE:
                       Yavasla = False
                       elFreni = True
                       Hizlan = False

               if olay.type == KEYUP:
                  if olay.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                  if olay.key == K_LEFT:
                        gitSola = False
                  if olay.key == K_RIGHT:
                        gitSaga = False
                #Sağ ok tuşundan elimizi çektiğimizde arabaBelir'i False yapıyoruz
                        arabaBelir = False

                  if olay.key == K_UP:
                        Hizlan = False
                        Yavasla = True
                #Yukarı ok tuşundan elimiz çektiğimizde sariArabaBelir'i False yapıyoruz
                        sariArabaBelir = False
                #arabaBelir'i yukarı ok tuşundan elimizi çektiğimizde False yapıyoruz
                        arabaBelir = False

                  if olay.key == K_DOWN:
                      gitAsagi = False
                      elFreni = False
                  if olay.key == K_SPACE:
                      Yavasla = True
                      elFreni = False


        if Hiz == 20:
             Hizlan = False

        if araba.right >= 640 or araba.left <= 160:
             YolDisi = True
        if araba.right < 640 and araba.left > 160:
             YolDisi = False

        if Hizlan and Hiz < 20:
              if araba.right < 640 and araba.left > 160:
                Hiz += 0.08
              else:
                 Hiz -= 0.05
        if Yavasla:
              if Hiz <= 1:
                 Hiz = 0
              else:
                 Hiz -= 0.05
        if YolDisi:
              if Hiz <= 1:
                 Hiz = 1
              else:
                 Hiz -= 0.1
        if elFreni:
              if Hiz > 0.3:
                 Hiz -= 0.3
              if Hiz <= 0.5:
                 Hiz = 0
        if Hiz >= 3:
              yanHiz = Hiz / 3
        else:
              yanHiz = Hiz
        if Hiz == 0:
              gitYukari = False


        #Sarı arabalar için oluşturduğumuz sayacı ne zaman durduracağımızı belirtiyoruz
        if sariArabaBelir and Hiz > 12:
              sariRakipSayac += 1
        if sariRakipSayac == sariRakip:
              sariRakipSayac = 0
              #Yeni araba eklemek için yeniAraba diye kendi oluşturduğumuz bir yapıya değişken oluşturuyoruz
              yeniAraba = {'rect': pygame.Rect(random.randint(161, 589), -20, 60, 100), 'speed': random.randint(10,19)}
              #Aynı koordinatlarda başka araba olup olmadığına bakıyoruz
              #Eğer aynı koordinatlarda başka araba varsa koordinatlaru değiştiriyoruz
              for b in sariArabalar:
                 while b['rect'].left in range(yeniAraba['rect'].left, yeniAraba['rect'].right) or b['rect'].right in       range(yeniAraba['rect'].left, yeniAraba['rect'].right):
                    yeniAraba = {'rect': pygame.Rect(random.randint(161, 589), -20, 60, 100), 'speed':       random.randint(10,19)}
              #Yeni arabamızı sariArabalar[] dizisine ekliyoruz
              sariArabalar.append(yeniAraba)

              
        #Arabanın yukarıdan aşağıya doğru hareketini sağlar
        for b in sariArabalar:
              b['rect'].move_ip(0, Hiz - b['speed'])

              
        #Aynı işlemlerin beyaz ve kırmızı arabalar için tekrarını yapıyoruz
        if sariArabaBelir and Hiz > 19:
              beyazRakipSayac += 1
        if beyazRakipSayac == beyazRakip:
              beyazRakipSayac = 0
              yeniAraba = {'rect': pygame.Rect(random.randint(161, 589), -20, 60, 100), 'speed': random.randint(10,19)}
              for b in beyazArabalar:
                 while b['rect'].left in range(yeniAraba['rect'].left, yeniAraba['rect'].right) or b['rect'].right in       range(yeniAraba['rect'].left, yeniAraba['rect'].right):
                    yeniAraba = {'rect': pygame.Rect(random.randint(161, 589), -20, 60, 100), 'speed':       random.randint(10,19)}

              beyazArabalar.append(yeniAraba)
        for b in beyazArabalar:
              b['rect'].move_ip(0, Hiz - b['speed'])


        if arabaBelir and Hiz > 10:
              rakipSayac += 1
        if rakipSayac == rakip:
              rakipSayac = 0
              yeniAraba = {'rect': pygame.Rect(random.randint(161, 589), -20, 60, 100), 'speed': random.randint(10,19)}
              for b in arabalar:
                 while b['rect'].left in range(yeniAraba['rect'].left, yeniAraba['rect'].right) or b['rect'].right in       range(yeniAraba['rect'].left, yeniAraba['rect'].right):
                    yeniAraba = {'rect': pygame.Rect(random.randint(161, 589), -20, 60, 100), 'speed':       random.randint(10,19)}
              arabalar.append(yeniAraba)
        for b in arabalar:
              b['rect'].move_ip(0, Hiz - b['speed'])


        #Çarpışma kontrolü
        for b in arabalar: #arabalar[] dizisindeki her arabanın sariArabalar[] içindeki
                                #arabalarla çarpışıp çarpışmadığını kontrol ediyoruz
              for c in sariArabalar:
                 if carpisma(b['rect'], c['rect']):#Çarpışma fonksiyonu True dönerse
                    #Çarpışan arabaların ekranda görünüp görünmediğine bakıyoruz
                    #Ekranda görünüyorlarsa Hızlarını 0 yapıyoruz
                    if b['rect'].bottom > 0 or c['rect'].bottom > 0:
                       b['rect'].move_ip(0, Hiz)
                       c['rect'].move_ip(0, Hiz)
                    else:
                       sariArabalar.remove(c)#Arabalar oluştukları anda çarpışıyorsa arabanın birini siliyoruz 
              #Aynı kontrolü beyaz arabalar için yapıyoruz
              for d in beyazArabalar:
                 if carpisma(b['rect'], d['rect']):
                    if b['rect'].bottom > 0 or c['rect'].bottom > 0:
                       b['rect'].move_ip(0, Hiz)
                       d['rect'].move_ip(0, Hiz)
                    else:
                       beyazArabalar.remove(d)
        for b in sariArabalar:
              for c in beyazArabalar:
                 if carpisma(b['rect'], c['rect']):
                    if b['rect'].bottom > 0 or c['rect'].bottom > 0:
                       b['rect'].move_ip(0, Hiz)
                       c['rect'].move_ip(0, Hiz)
                    else:
                       sariArabalar.remove(b)

        #Kullanıcı arabasının kontrolü
        #Rakip arabaların kullanıcının arabasıyla çarpışıp çarpışmadığını kontrol ediyoruz
        for b in arabalar:
              if carpisma(araba, b['rect']) and araba.top > b['rect'].top:
                 Hiz = 0
                 yanHiz = 0
              elif carpisma(araba, b['rect']):
                 Hiz = 1
                 yanHiz = 0
                 b['speed'] = 0
        for b in sariArabalar:
              if carpisma(araba, b['rect']) and araba.top > b['rect'].top:
                 Hiz = 0
                 yanHiz = 0
              elif carpisma(araba, b['rect']):
                 Hiz = 1
                 yanHiz = 0
                 b['speed'] = 0
        for b in beyazArabalar:
              if carpisma(araba, b['rect']) and araba.top > b['rect'].top:
                 Hiz = 0
                 yanHiz = 0
              elif carpisma(araba, b['rect']):
                 Hiz = 1
                 yanHiz = 0
                 b['speed'] = 0




        if gitAsagi:
              if yol.bottom > pencereYuksek:
                 yol.bottom -= Hiz
        if gitYukari:
              if yol.top < 0:
                 yol.top += Hiz
              else:
                 yol.top = -180
        if gitSaga and araba.right < pencereGenis:
              if gitYukari or gitAsagi:
                 araba.right += yanHiz
        if gitSola and araba.left > 0:
              if gitYukari or gitAsagi:
                 araba.left -= yanHiz

        pencereYuzeyi.blit(yolResim, yol)
        yaziYaz('HIZ: %s ' % (int(10 * Hiz)), tip, pencereYuzeyi, 170, 0)
        pencereYuzeyi.blit(bariyer, sagBariyer)
        pencereYuzeyi.blit(bariyer, solBariyer)
        pencereYuzeyi.blit(arabaResim, araba)
        #Tüm arabaların ekrana çizdirilmesi
        for b in arabalar:
              pencereYuzeyi.blit(araba1Resim, b['rect'])
        for b in sariArabalar:
              pencereYuzeyi.blit(araba3Resim, b['rect'])
        for b in beyazArabalar:
              pencereYuzeyi.blit(araba2Resim, b['rect'])

        pygame.display.update()
        saat.tick(40)
