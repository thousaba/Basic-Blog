import json
from datetime import datetime

# --- POST SINIFI ---
class Post:
    def __init__(self, baslik, icerik, yazar):
        self.baslik = baslik
        self.icerik = icerik
        self.yazar = yazar
        self.tarih = datetime.now().strftime("%Y-%m-%d %H:%M")

    def to_dict(self):
        return {
            "baslik": self.baslik,
            "icerik": self.icerik,
            "yazar": self.yazar,
            "tarih": self.tarih
        }

    @staticmethod
    def from_dict(data):
        post = Post(data["baslik"], data["icerik"], data["yazar"])
        post.tarih = data["tarih"]
        return post


# --- KULLANICI SINIFI ---
class User:
    def __init__(self, kullanici_adi, sifre):
        self.kullanici_adi = kullanici_adi
        self.sifre = sifre


# --- BLOG YÖNETİMİ ---
class BlogYonetimi:
    def __init__(self):
        self.yazilar = []
        self.verileri_yukle()

    def yeni_yazi_ekle(self, baslik, icerik, yazar):
        yeni_post = Post(baslik, icerik, yazar)
        self.yazilar.append(yeni_post)
        self.verileri_kaydet()
        print(f"\n'{baslik}' başlıklı yazı eklendi.\n")

    def tum_yazilari_listele(self):
        if not self.yazilar:
            print("\nHenüz hiç yazı eklenmedi.\n")
            return
        print("\n=== Blog Yazıları ===\n")
        for i, post in enumerate(self.yazilar):
            print(f"{i + 1}. {post.baslik} - {post.yazar} ({post.tarih})")
        print()

    def yazi_detayi_goster(self, index):
        try:
            post = self.yazilar[index - 1]
            print("\n=== Yazı Detayı ===")
            print(f"Başlık: {post.baslik}")
            print(f"Yazar: {post.yazar}")
            print(f"Tarih: {post.tarih}")
            print(f"İçerik: {post.icerik}")
            print("==================\n")
        except IndexError:
            print("\nGeçersiz numara!\n")

    def yazi_sil(self, index):
        try:
            silinen = self.yazilar.pop(index - 1)
            print(f"\n'{silinen.baslik}' başlıklı yazı silindi.\n")
            self.verileri_kaydet()
        except IndexError:
            print("\nGeçersiz numara!\n")

    def verileri_kaydet(self, dosya="blog_data.json"):
        with open(dosya, "w") as f:
            json.dump([post.to_dict() for post in self.yazilar], f, indent=4)

    def verileri_yukle(self, dosya="blog_data.json"):
        try:
            with open(dosya, "r") as f:
                veri = json.load(f)
                for item in veri:
                    self.yazilar.append(Post.from_dict(item))
        except (FileNotFoundError, json.JSONDecodeError):
            pass


# --- KULLANICI YÖNETİMİ ---
class KullaniciYonetimi:
    def __init__(self):
        self.kullanicilar = []
        self.giris_yapmis_kullanici = None
        self.verileri_yukle()

    def kullanici_kaydet(self, kullanici_adi, sifre):
        for u in self.kullanicilar:
            if u.kullanici_adi == kullanici_adi:
                print("\nBu kullanıcı adı zaten alınmış.\n")
                return
        self.kullanicilar.append(User(kullanici_adi, sifre))
        self.verileri_kaydet()
        print(f"\n'{kullanici_adi}' başarıyla kaydedildi!\n")

    def kullanici_girisi(self, kullanici_adi, sifre):
        for u in self.kullanicilar:
            if u.kullanici_adi == kullanici_adi and u.sifre == sifre:
                self.giris_yapmis_kullanici = u
                print(f"\nHoş geldin {u.kullanici_adi}!\n")
                return True
        print("\nGeçersiz kullanıcı adı veya şifre.\n")
        return False

    def verileri_kaydet(self, dosya="blog_users.json"):
        with open(dosya, "w") as f:
            json.dump(
                [{"kullanici_adi": u.kullanici_adi, "sifre": u.sifre} for u in self.kullanicilar],
                f,
                indent=4
            )

    def verileri_yukle(self, dosya="blog_users.json"):
        try:
            with open(dosya, "r") as f:
                veri = json.load(f)
                for item in veri:
                    self.kullanicilar.append(User(item["kullanici_adi"], item["sifre"]))
        except (FileNotFoundError, json.JSONDecodeError):
            pass


# --- ANA MENÜ ---
def ana_menu():
    print("=== Basit Blog Sistemi ===")
    print("1. Üye Ol")
    print("2. Giriş Yap")
    print("3. Yazı Ekle")
    print("4. Tüm Yazıları Listele")
    print("5. Yazı Detaylarını Görüntüle")
    print("6. Yazı Sil")
    print("7. Çıkış")
    secim = input("Seçiminizi yapın (1-7): ")
    return secim


# --- ANA PROGRAM ---
def main():
    kullanici_yonetimi = KullaniciYonetimi()
    blog_yonetimi = BlogYonetimi()

    while True:
        secim = ana_menu()

        if secim == "1":
            kullanici = input("Kullanıcı Adı: ")
            sifre = input("Şifre: ")
            kullanici_yonetimi.kullanici_kaydet(kullanici, sifre)

        elif secim == "2":
            kullanici = input("Kullanıcı Adı: ")
            sifre = input("Şifre: ")
            kullanici_yonetimi.kullanici_girisi(kullanici, sifre)

        elif secim == "3":
            if kullanici_yonetimi.giris_yapmis_kullanici:
                baslik = input("Yazı Başlığı: ")
                icerik = input("Yazı İçeriği: ")
                yazar = kullanici_yonetimi.giris_yapmis_kullanici.kullanici_adi
                blog_yonetimi.yeni_yazi_ekle(baslik, icerik, yazar)
            else:
                print("\nYazı eklemek için önce giriş yapmalısınız.\n")

        elif secim == "4":
            blog_yonetimi.tum_yazilari_listele()

        elif secim == "5":
            blog_yonetimi.tum_yazilari_listele()
            try:
                index = int(input("Detayını görmek istediğiniz yazının numarası: "))
                blog_yonetimi.yazi_detayi_goster(index)
            except ValueError:
                print("\nLütfen geçerli bir sayı girin.\n")

        elif secim == "6":
            if not kullanici_yonetimi.giris_yapmis_kullanici:
                print("Yazı silmek için giriş yapmalısınız!")
                continue
            
            blog_yonetimi.tum_yazilari_listele()
            try:
                index = int(input("Silmek istediğiniz yazının numarası: "))
                post= blog_yonetimi.yazilar[index -1]
                if post.yazar == kullanici_yonetimi.giris_yapmis_kullanici.kullanici_adi:
                    blog_yonetimi.yazi_sil(index)
                else:
                    print("Bu yazıyı silmeye yetkiniz yoktur!")    

            except (ValueError, IndexError):
                print("\nLütfen geçerli bir sayı girin.\n")

        elif secim == "7":
            print("\nProgramdan çıkılıyor...")
            break

        else:
            print("\nGeçersiz seçim. Lütfen 1-7 arasında bir sayı girin.\n")


# --- PROGRAMI BAŞLAT ---
if __name__ == "__main__":
    main()