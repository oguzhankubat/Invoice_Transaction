import os
import time as tm
import sys
from colorama import Fore, init
import re
import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import logging
import json

logger = logging.getLogger(__name__)

logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler("SİSTEM\\program_log.txt")

formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.info("---------------------------------------------------------")
logger.info("Program başladı")

#Fore.BLACK, Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE,
#Fore.MAGENTA, Fore.CYAN, Fore.WHITE      RENKLER
init(autoreset=True)#coloramayı başlatma kodu
#Style.RESET_ALL tüm renkleri sıfırlar

kok_dizin = os.getcwd()
dosya_yolu = os.path.join(kok_dizin, "SİSTEM\\Fatura Listesi(DOSYAYI AÇMAYIN).txt")
dosya_yolu_2=os.path.join(kok_dizin, "SİSTEM\\maksimum_hesap_sayisi.txt")
dosya_yolu_3=os.path.join(kok_dizin, "SİSTEM\\kullanici_bilgileri.txt")
dosya_yolu_4=os.path.join(kok_dizin, "SİSTEM\\guncelleme_bildirim_kontrol.txt")
dosya_yolu_5=os.path.join(kok_dizin, "SİSTEM\\hatalar.txt")
klasor_adi = "SİSTEM"


klasor_yolu = os.path.join(kok_dizin, klasor_adi)

try:

    def anlik_zamani_kaydet():
        return tm.strftime("%d-%m-%Y %H:%M:%S")
        
    def hata_kaydet(hata_mesaji):
        anlik_zaman=anlik_zamani_kaydet()
        with open(dosya_yolu_5, "a") as dosya:
            dosya.write("\nÇökme nedeni: "+hata_mesaji +"  "+  "---------" + "    "+anlik_zaman+ "\n")
    def ekran_temizle():
        os.system("cls" if os.name == "nt" else "clear")        
    def clear_screen():
        if os.name == "posix":
            _ = os.system("clear")
        else:
            _ = os.system("cls")
    def maksimum_hesap_sayisi_belirle():
    
        while True:
            clear_screen()
            if not os.path.exists(klasor_yolu):
                os.mkdir(klasor_yolu)
            else:
                pass
            print(f"\n\n\n\n\n\n\n\n\n\n\n\n\n                                                                    {Fore.YELLOW}***BİLGİLENDİRME***\n\n                                         {Fore.WHITE}Bu Aşama Bir Kez Belirlenecektir. {Fore.YELLOW}Yeniden Düzenleme Hakkınız Olmayacaktır.{Fore.WHITE}")
            maksimum_hesap_sayisi = input(f"\n\n\n                                                   Oluşturabilecek{Fore.YELLOW} Maksimum{Fore.WHITE} Hesap Sayısını Belirleyin: ")
    
            if not maksimum_hesap_sayisi.isdigit() or int(maksimum_hesap_sayisi)<=0:
                print(f"\n\n                                                            {Fore.YELLOW}Lütfen pozitif bir tam sayı giriniz!{Fore.WHITE}")
                tm.sleep(3)
                continue
    
            with open(dosya_yolu_2, "w") as dosya:
                dosya.write(str(maksimum_hesap_sayisi))
            
            print(f"\n\n                                                        Maksimum Hesap Sayısı {Fore.YELLOW}{maksimum_hesap_sayisi}{Fore.WHITE} Olarak {Fore.YELLOW}BELİRLENDİ.{Fore.WHITE}")
            tm.sleep(2)
            clear_screen()
            break
    
    
    
    def sifre_kontrol(sifre):
    
        if len(sifre) < 8:
            return False
        
    
        if not any(c.isupper() for c in sifre) or not any(c.islower() for c in sifre):
            return False
        
        return True
    def kullanici_adi_kontrol(kullanici_adi):
        if kullanici_adi.strip() == "":
            print(f"\n\n                                                     {Fore.YELLOW}Kullanıcı Adı Boş BIRAKILAMAZ!!{Fore.WHITE}")
            tm.sleep(3)
            clear_screen()
            return False
        if " " in kullanici_adi:
            print(f"\n\n                                                       {Fore.YELLOW}Kullanıcı Adı Boş Karakter İÇEREMEZ!!{Fore.WHITE}")
            tm.sleep(3)
            clear_screen()
            return False
        return True
        
    def hesap_olustur():
        logger.info("Hesap oluşturma alanı açıldı.")
        sifre=None
        if not os.path.exists(dosya_yolu_2) or os.stat(dosya_yolu_2).st_size == 0:
            maksimum_hesap_sayisi_belirle()
        clear_screen()
        while True:
            clear_screen()
            kullanici_adi = input(f"\n\n\n\n\n\n\n\n\n\n\n\n\n                                                          {Fore.YELLOW}Yeni Kullanıcı Adı:{Fore.WHITE} ")
    
            if not kullanici_adi_kontrol(kullanici_adi):
                continue
                
            sifre = input(f"\n                                                          {Fore.YELLOW}Şifre:{Fore.WHITE} ")
            onay=input(f"\n\n                                     Yukarıda Girilen Kullanıcı Adı ve Şifreyi Onaylıyor Musunuz? {Fore.YELLOW}Evet/Hayır:{Fore.WHITE}  ").lower()
            if onay=="evet":
                break
            else:
                continue
        with open(dosya_yolu_2, "r") as dosya:
            maksimum_hesap_sayisi = int(dosya.read().strip())
    
        try:
            with open(dosya_yolu_3, "r") as dosya:
                kullanicilar = dosya.readlines()
        except FileNotFoundError:
            kullanicilar = []
    
        toplam_hesap_sayisi = sum(1 for kullanici in kullanicilar)
    
        if toplam_hesap_sayisi >= maksimum_hesap_sayisi:
            print(f"\n\n                                        Maksimum Hesap Sayısına Ulaşıldı {Fore.YELLOW}({maksimum_hesap_sayisi}){Fore.WHITE}. Yeni bir Hesap {Fore.YELLOW}OLUŞTURULAMAZ{Fore.RED} !!{Fore.WHITE}")
            tm.sleep(4)
            return
    
        kullanici_var_mi = any(kullanici_adi == veri.strip().split()[0] for veri in kullanicilar)
    
        if kullanici_var_mi:
            print(f"\n\n                                        {Fore.YELLOW}Bu Kullanıcı Adı Zaten Kullanılıyor!{Fore.WHITE} Lütfen Başka Bir Kullanıcı Adı Seçin.")
            tm.sleep(3)
        else:
            if sifre is not None and sifre_kontrol(sifre):
                with open(dosya_yolu_3, "a") as dosya:
                    dosya.write(f"{kullanici_adi} {sifre}\n")
                    logger.info("Hesap oluşturuldu. | {kullanici_adi}  {sifre}")
                print(f"\n\n                                                   Hesap {Fore.GREEN}BAŞARILI{Fore.WHITE} Bir Şekilde {Fore.YELLOW}Oluşturuldu.{Fore.WHITE}")
                tm.sleep(4)
            else:
                print(f"\n\n                                                   {Fore.RED}Şifre İstenilen Kriterleri Karşılamıyor!{Fore.WHITE}\n\n                              {Fore.YELLOW}Şifre en az 8 karakter uzunluğunda ve en az bir büyük harf ve bir küçük harf içermelidir.{Fore.WHITE}")
                tm.sleep(6)
 
    def kimlik_dogrula():
        if not os.path.exists(dosya_yolu_3):
            print(f"\n\n\n                                           {Fore.YELLOW}Sistemde{Fore.WHITE} Kayıtlı Kullanıcı Hesabı {Fore.YELLOW}BULUNMAMAKTADIR!{Fore.WHITE} Lütfen Hesap Oluşturun.")
            tm.sleep(4)
            giris()
        def check_password():
            global entered_username
            entered_username = username_entry.get()
            entered_password = password_entry.get()
    
            with open(dosya_yolu_3, "r") as dosya:
                kullanicilar = dosya.readlines()
    
            for kullanici in kullanicilar:
                veriler = kullanici.strip().split()
                if entered_username == veriler[0] and entered_password == veriler[1]:
                    bosluk()
                    app.destroy()  
                    yukleniyor_cubugu_2(2)
                    return True,entered_username
            
    
            messagebox.showerror("Hata", "Giriş Bilgileri Geçersiz.\n\nBilgilerini Kontrol Ediniz!")
    
        app = tk.Tk()
        app.title("Kimlik Doğrulama")
        window_width = 330
        window_height = 170
        screen_width = app.winfo_screenwidth()
        screen_height = app.winfo_screenheight()
        x = (screen_width / 2) - (window_width / 2)
        y = (screen_height / 2) - (window_height / 2)
        app.geometry(f"{window_width}x{window_height}+{int(x)}+{int(y)}")
    
        username_label = tk.Label(app, text="Kullanıcı Adı:")
        username_label.pack()
    
        username_entry = tk.Entry(app)
        username_entry.pack()
    
        password_label = tk.Label(app, text="Şifre:")
        password_label.pack()
    
        password_entry = tk.Entry(app, show="*")
        password_entry.pack()
    
        
        submit_button = tk.Button(app, text="Giriş", command=check_password)
        submit_button.pack()
        submit_button.place(relx=0.5, rely=0.7, anchor="center")
    
        app.protocol("WM_DELETE_WINDOW", lambda: sys.exit())
    
        app.mainloop()
    def yukleniyor_cubugu_3():
        chars = ""
        bosluk()
        for i in range(6):
            chars += "."
            sys.stdout.write(f"\r{Fore.YELLOW}" + chars)
            sys.stdout.flush()
            tm.sleep(0.2)
        print(f"\n\n\n\n{Fore.YELLOW}İlgili Ekran YÜKLENİYOR.{Fore.WHITE}")
        tm.sleep(1)
    def yukleniyor_cubugu_2(seconds):
        chars = "|/-\\"
        for i in range(seconds*5):
            sys.stdout.write(f"\r                                                                     {Fore.GREEN}Giriş BAŞARILI... " + chars[i % len(chars)])
            sys.stdout.flush()
            tm.sleep(0.2)
    
        sys.stdout.write(f"\n\n\r                                            \n")
        tm.sleep(0.4)
    
    
    def sayiyi_turkceye_cevir(sayi):
        birler = ["", "bir", "iki", "üç", "dört", "beş", "altı", "yedi", "sekiz", "dokuz"]
        onlar = ["", "on", "yirmi", "otuz", "kırk", "elli", "altmış", "yetmiş", "seksen", "doksan"]
        
        if '.' in sayi:
            tam_kisim, ondalik_kisim = sayi.split(".")
        else:
            tam_kisim = sayi
            ondalik_kisim = '0'
        
        tam_kisim = int(tam_kisim.replace(",", ""))
        tam_kisim_str = ""
        if tam_kisim == 0:
            tam_kisim_str = "sıfır"
        else:
            milyarlar = tam_kisim // 1000000000
            milyonlar = (tam_kisim % 1000000000) // 1000000
            binler = (tam_kisim % 1000000) // 1000
            yuzler = (tam_kisim % 1000) // 100
            onlar_basamagi = (tam_kisim % 100) // 10
            birler_basamagi = tam_kisim % 10
            
            if milyarlar > 0:
                if milyarlar > 9:
                    tam_kisim_str += sayiyi_turkceye_cevir(str(milyarlar)) + "milyar".capitalize()
                else:
                    tam_kisim_str += birler[milyarlar] + "milyar".capitalize()
            if milyonlar > 0:
                if milyonlar > 9:
                    tam_kisim_str += sayiyi_turkceye_cevir(str(milyonlar)) + "milyon".capitalize()
                else:
                    tam_kisim_str += birler[milyonlar] + "milyon".capitalize()
            if binler > 0:
                if binler > 9:
                    tam_kisim_str += sayiyi_turkceye_cevir(str(binler)) + "bin".capitalize()
                else:
                    tam_kisim_str += birler[binler] + "bin".capitalize()
            if yuzler > 0:
                tam_kisim_str += birler[yuzler] + "yüz".capitalize() if yuzler != 1 else "yüz".capitalize()
            if onlar_basamagi > 0:
                tam_kisim_str += onlar[onlar_basamagi]
            if birler_basamagi > 0:
                tam_kisim_str += birler[birler_basamagi]
        
        ondalik_kisim = ondalik_kisim.split()[0]
        ondalik_kisim_str = sayiyi_turkceye_cevir(ondalik_kisim) if ondalik_kisim != '0' else ''
        return tam_kisim_str + (" Lira " + ondalik_kisim_str + " Kurus" if ondalik_kisim_str else '')
    
    
    def filter_invoices_by_date(invoices, start_date, end_date):
        filtered_invoices = []
        for invoice in invoices:
            invoice_date = datetime.strptime(invoice['Tarih'], "%d.%m.%Y") 
            if start_date <= invoice_date <= end_date:
                filtered_invoices.append(invoice)
        return filtered_invoices
    def bosluk():
        print("")
        print("")
        print("")
        print("")
    def filter_invoices_by_amount(invoices, min_amount, max_amount):
        filtered_invoices = []
        for invoice in invoices:
            invoice_amount = float(invoice['Fatura Tutarı'].split()[0])
            if min_amount <= invoice_amount <= max_amount:
                filtered_invoices.append(invoice)
        return filtered_invoices
    def is_valid_date(date_str):
        date_pattern = r"^\d{2}\.\d{2}.\d{4}$"
        return re.match(date_pattern, date_str) is not None
    
    
    def yukleniyor_cubugu(seconds):
        chars = "|/-\\"
        for i in range(seconds*5):
            sys.stdout.write(f"\rSizin için arka planda çalışıyoruz. {Fore.YELLOW}LÜTFEN BEKLEYİNİZ... " + chars[i % len(chars)])
            sys.stdout.flush()
            tm.sleep(0.2)
    
        sys.stdout.write(f"\n\n\r{Fore.GREEN}               Yüklenme TAMAMLANDI!                                             \n")
        tm.sleep(1)
    
    def bilgilendirme():
        logger.info("Program başlangıcında bilgilendirme açıldı.")
        clear_screen()
        print(f"""\n\n\nProgramda yazılanları doğru bir şekilde görüntüleyemiyorsanız:\n\n
                  {Fore.YELLOW}1-{Fore.WHITE} Programı açın.\n\n
                  {Fore.YELLOW}2-{Fore.WHITE} py.exe yazan KALIN BEYAZ kısma gelip SAĞ tık yapın.\n\n
                  {Fore.YELLOW}3-{Fore.WHITE} Varsayılanlar'a tıklayın.\n\n
                  {Fore.YELLOW}4-{Fore.WHITE} Yerleşim sekmesine gelin.\n\n
                  {Fore.YELLOW}5-{Fore.WHITE} Pencere Boyutu; GENİŞLİK: 160 YÜKSEKLİK: 45 Şeklinde düzenleyip 'Tamam'a basınız.\n\n
                  {Fore.YELLOW}6-{Fore.WHITE} Programı tekrar başlatın.
        """)
        input(f"\n\n\nPrograma Geri Dönmek için {Fore.YELLOW}'Enter'{Fore.WHITE} basınız: ")
        logger.info("Bilgilendirme alanı kapatıldı.")
    def extract_number(text):
        try:
            return float(text.split()[0])
        except ValueError:
            return None
        
    def format_number(number):
                try:
                    number = float(number)
                    formatted_number = "{:,.2f}".format(number)
                    return formatted_number
                except ValueError:
                    return "Geçersiz Giriş"
    
    def search_invoices_by_name(invoice_list, target_name):
        found_invoices = []
    
        for invoice in invoice_list:
            if target_name.lower() in invoice['Firma İsmi'].lower():
                found_invoices.append(invoice)
    
        return found_invoices
    
    def miktar_kontrol():
        
        while True:
            
            min_amount = input(f"\n\nMinimum Fatura Tutarı {Fore.YELLOW}(Varsayılan: 0){Fore.WHITE}: ")
            max_amount = input(f"\n\nMaksimum Fatura Tutarı {Fore.YELLOW}(Varsayılan: 99,999,999,999,999,999.00){Fore.WHITE}: ")
                                    
            if min_amount and not min_amount.isdigit() or max_amount and not max_amount.isdigit():
                print(f"\n                                                        {Fore.RED}GEÇERSİZ TUTAR FORMATI!!{Fore.YELLOW} Sadece sayısal değerleri GİREBİLİRSİNİZ.{Fore.WHITE}")
                continue
                                    
            if min_amount:
                min_amount = float(min_amount)
            else:
                min_amount = 0
                                    
            if max_amount:
                max_amount = float(max_amount)
            else:
                max_amount = 99_999_999_999_999_999
                                    
            if min_amount >= max_amount:
                print(f"\n\n                                                                 {Fore.YELLOW}Minimum tutar, Maksimum tutar'dan {Fore.RED}BÜYÜK ya da AYNI OLAMAZ!!{Fore.WHITE}")
                continue
            logger.info(f"Tutar aralığı girildi. {min_amount} | {max_amount}")
            return (min_amount, max_amount, True)
        
    def tarih_kontrol():
        while True:
            start_date = input(f"\n\nBaşlangıç Tarihi {Fore.YELLOW}(GG.MM.YYYY):{Fore.WHITE} ")
            end_date = input(f"\n\nBitiş Tarihi {Fore.YELLOW}(GG.MM.YYYY):{Fore.WHITE} ")
    
            if not is_valid_date(start_date) or not is_valid_date(end_date):
                print(f"                                                                 {Fore.RED}GEÇERSİZ TARİH FORMATI!!{Fore.YELLOW} Lütfen GG.MM.YYYY formatında girin.{Fore.WHITE}")
                continue
    
            try:
                start_datetime = datetime.strptime(start_date, "%d.%m.%Y")
                end_datetime = datetime.strptime(end_date, "%d.%m.%Y")
            except ValueError:
                print(f"                                                                 {Fore.RED}GEÇERSİZ TARİH FORMATI!!{Fore.YELLOW} Lütfen 31.12.9999 formatında girin.{Fore.WHITE}")
                continue
    
            if start_datetime >= end_datetime:
                print(f"                                                       {Fore.YELLOW}Başlangıç Tarihi, Bitiş Tarihinden {Fore.RED}BÜYÜK Ya da AYNI OLAMAZ{Fore.WHITE}")
                continue
            logger.info(f"Tarih aralığı girildi. {start_date} | {end_date}")
            return (start_datetime, end_datetime, True)
    def tarih_miktar_kontrol():
        result=tarih_kontrol()
        start,end,kontrol1=result
        
        result2=miktar_kontrol()
        min_a,max_a,kontrol2=result2
        if kontrol1 and kontrol2:
            return start,end,min_a,max_a,True
        else:
            
            return False
        
    def ana_menu():
        
        logger.info("Ana menü görüntülendi.")
        yukleniyor_cubugu_3()
        
        tm.sleep(1)
        clear_screen()
        guncelleme_bildirme()
        clear_screen()
        print("\n\n\n\n\n\n\n\n\n\n                                                                   ---İşlem Seçenekleri---")
        print(f"\n\n                                                                     {Fore.YELLOW}1-{Fore.WHITE} Fatura Kaydetme")
        print(f"\n                                                                     {Fore.YELLOW}2-{Fore.WHITE} Fatura Ödeme")
        print(f"\n                                                                     {Fore.YELLOW}3-{Fore.WHITE} Fatura Silme")
        print(f"\n                                                                     {Fore.YELLOW}4-{Fore.WHITE} Fatura Bulma")
    
        cevap = input("\n\n                                                                 Lütfen işlem tipini seçin: ")
        print(f"\n\n{Fore.YELLOW}                                                                 İşlem Gerçekleştiriliyor...")
        tm.sleep(1)
        match cevap:
            case "1":
                clear_screen()
                main_fatura_kaydetme()
            case "2":
                clear_screen()
                main()
            case "3":
                clear_screen()
                ana_program_silme()
            case "4":
                clear_screen()
                main_fatura_bulma()
            case _:
                logger.info("Hatalı işlem seçeneği seçildi.")
                print("\n\n                                                                      Geçersiz Giriş")
                tm.sleep(2)
                ana_menu()
                
    
    def giris():
        logger.info("Giriş ekranı açıldı.")
        while True:
            clear_screen()
            print(f"\n\n\n\n\n\n\n\n\n\n\n\n\n                                                                {Fore.YELLOW}---KULLANICI GİRİŞ EKRANI---{Fore.WHITE}")
            print(f"\n\n                                                                        {Fore.YELLOW}1-{Fore.WHITE} Giriş")
            print(f"\n                                                                      {Fore.YELLOW}2-{Fore.WHITE} Hesap Oluştur")
            print(f"\n                                                                        {Fore.YELLOW}3-{Fore.WHITE} Çıkış")
    
            secim = input(f"\n\n\n                                                                  Seçiminizi yapın {Fore.YELLOW}(1/2/3){Fore.WHITE}: ")
            logger.info(f"Kullanıcı Giriş Ekranı Secimi: {secim}")
            match secim:
                case "1":
                    logger.info("Kimlik dogruma işlemine geçildi.")
                    kimlik_dogrula()
                    if kimlik_dogrula:
                        logger.info(f"Giriş başarılı.  | Kullanıcı Adı: {entered_username}")
                        ana_menu()
                case "2":
                    logger.info("Hesap oluşturma adımına geçildi.")
                    hesap_olustur()
                case "3":
                    logger.info("Program sonlandırıldı.")
                    print("\n\nProgram Sonlandırıldı.")
                    tm.sleep(2)
                    sys.exit()
                case _:
                    print(f"\n\n\n                                                            {Fore.YELLOW}Geçersiz SEÇİM! Lütfen Tekrar Deneyin.{Fore.WHITE}")
                    tm.sleep(3)
                    clear_screen()
                    continue
    def print_invoices(invoices, title, total, show_total=True):
        logger.info(f"Faturalar görüntülendi.")
        print(f"\n{title}")
        for index, invoice in enumerate(invoices, start=1):
            logger.info(f"{index}- {invoice}")
            if invoice['Durum'].startswith("Durum: [32mÖdendi"):
                renk = f"{Fore.GREEN}"
            else:
                renk = f"{Fore.RED}"
    
            print(f"\n  {Fore.YELLOW}{index}. Fatura {Fore.WHITE}\n\nTarih: {Fore.YELLOW}{invoice['Tarih']}{Fore.WHITE} \nFirma İsmi: {Fore.CYAN}{invoice['Firma İsmi']}{Fore.WHITE}\n\nFatura İçeriği:{Fore.YELLOW} {invoice['Fatura İçeriği']}\n\n{Fore.WHITE}Fatura Tutarı: {renk}{format_number(float(invoice['Fatura Tutarı'].split()[0]))} {Fore.WHITE}Türk Lirası {Fore.WHITE}                                                   |  {sayiyi_turkceye_cevir(invoice['Fatura Tutarı'])}\n{invoice['Durum']}\n")
            print("---------------------------------------------------------")
    
        if show_total:
            unpaid_count = sum(1 for invoice in invoices if "Ödendi" not in invoice['Durum'])
            unpaid_total = sum(extract_number(invoice['Fatura Tutarı']) for invoice in invoices if "Ödendi" not in invoice['Durum'])
    
            unpaid_invoice_info = (
                f"""
 {Fore.YELLOW}{index}. Fatura - {Fore.CYAN}{invoice['Firma İsmi']} {Fore.YELLOW}[{format_number(float(invoice['Fatura Tutarı'].split()[0]))} Türk Lirası] [{invoice['Tarih']}]
 -----------------------------------------------------------
                """
                for index, invoice in enumerate(invoices, start=1)
                if "Ödendi" not in invoice['Durum']
            )
            if unpaid_invoice_info:
                unpaid_invoice_info_str = "\n".join(unpaid_invoice_info)
                
    
            company_names = {invoice['Firma İsmi'] for invoice in invoices if "Ödendi" not in invoice['Durum']}
            company_names_str = ", ".join(sorted(company_names))
    
            if unpaid_count > 0:
                print(f"\n  {Fore.RED}ÖDENMEMİŞ{Fore.WHITE} Faturaların {Fore.YELLOW}ÖZET{Fore.WHITE} Bilgileri:                                      {Fore.WHITE}| DETAYLI BİLGİ YUKARIDADIR.{Fore.YELLOW}\n{unpaid_invoice_info_str}")
                if "," in company_names_str:
                    unpaid_statement = f"\n | {Fore.CYAN}{company_names_str}{Fore.WHITE} |\n\n Adlı Firmalara ait Toplam {Fore.RED}ÖDENMEMİŞ{Fore.WHITE} Fatura Sayısı: {Fore.CYAN}{unpaid_count}"
                else:
                    unpaid_statement = f"\n | {Fore.CYAN}{company_names_str}{Fore.WHITE} | Adlı Firmaya ait Toplam {Fore.RED}ÖDENMEMİŞ{Fore.WHITE} Fatura Sayısı: {Fore.CYAN}{unpaid_count}"
            else:
                unpaid_statement = f"\n\n  {Fore.GREEN}Listelenen FATURALAR ÖDENMİŞTİR.{Fore.WHITE}"
                logger.info("Listelenen faturaların ödenmiş olduğu bilgisi verildi.")
                print(unpaid_statement)
                p=input(f"\n\n\nYeniden Arama İçin {Fore.YELLOW}'Tekrar'{Fore.WHITE} |  Çıkış İçin {Fore.YELLOW}'Enter' {Fore.WHITE} | Ana Menü için {Fore.YELLOW}'Menu'{Fore.WHITE} : ").lower()
                logger.info(f"Kullanıcı '{p}' seçimini seçti.")
                if "tek" in p:
                    print(f"\n\n\n{Fore.YELLOW}Lütfen Bekleyiniz...{Fore.WHITE}")
                    tm.sleep(2)
                    main()
                elif "menu" in p:
                    ana_menu()
                else:
                    print("\n\n\nProgram Sonlandırıldı.")
                    tm.sleep(2)
                    sys.exit()
    
            print(unpaid_statement)
    
            formatted_result = format_number(unpaid_total)
            print(f"""\n\n                                                                                         
 Listelenen {Fore.RED}ÖDENMEMİŞ{Fore.WHITE} Faturaların Toplamı: {Fore.YELLOW}{formatted_result } Türk Lirası""")
       
    def select_kontrol(secim):
        if 'off' in secim:
        
            clear_screen()
            logger.info("Program sonlandırıldı.")
            print("\n\nProgram sonlandırıldı.")
            tm.sleep(2)
            sys.exit()
        if 'tekrar' in secim:
            yukleniyor_cubugu_3()
            main()
    def indeks_sapta(secim,fonk,valid,invalid):
        for index in secim:
            
            if index.isnumeric():
                
                num_index = int(index)
                if 0 < num_index <= len(fonk):
                    
                    valid.append(num_index-1)
                else:
                    
                    invalid.append(index)
            else:
                
                invalid.append(index)
    
        valid.sort()  
    def fatura_yok():
        logger.info("Seçilen kriterlere ait fatura bulunamadı.")
        print(f"\n\n\nSeçilen Kriterlere Ait Fatura {Fore.YELLOW}BULUNAMADI.{Fore.WHITE}")
        tm.sleep(3)
        a=input(f"\n\n\nProgramı kapatmak için {Fore.YELLOW}'Enter'{Fore.WHITE} basınız, Yeniden Arama için {Fore.YELLOW}'Tekrar'{Fore.WHITE} yazınız : ").lower()
        if a=="tekrar":
            print(f"\n\n\n{Fore.YELLOW}Lütfen BEKLEYİNİZ...{Fore.WHITE}")
            tm.sleep(2)
            main()
        else:
            print("\n\nProgram 3 sn içinde kapanacaktır.")
            tm.sleep(3)
            sys.exit()
    
    def guncelleme_bildirme():
        
        try:
            with open(dosya_yolu_4, "r") as dosya:
                sayac = dosya.read()
        except FileNotFoundError:
            sayac = ""
        a=f"""\n\n\n\n                                                                 {Fore.YELLOW}Güncelleme Yapıldı.\n\n{Fore.WHITE}
    
    
                                     {Fore.YELLOW}Bu Sürüm İle;{Fore.WHITE}                                                           09.02.2024
                                     
    
                                     {Fore.YELLOW}1-{Fore.WHITE} Artık Tüm Fatura işlemleri Tek Çatı Altında Toplandı.
                                     
                                     {Fore.YELLOW}2-{Fore.WHITE} Çeşitli hata ve sistemsel iyileştirilmeler yapıldı.
    
                                     {Fore.YELLOW}3-{Fore.WHITE} Teyit sırasında hata yapıldığında aynı fatura için tekrar deneme imkanı sunuldu.
    
                                     {Fore.YELLOW}4-{Fore.WHITE} Sistemdeki Verilerin Anlık Güncellenmesi İyileştirildi.
    
                                     {Fore.YELLOW}5-{Fore.WHITE} Fatura Bulma ve Silme İşlemlerinde Önemli İyileştirmeler Yapıldı."""
        
        if sayac!=a:
            logger.info("Güncelleme bildirildi.")
            print(a)
            input(f"\n\n\nDevam etmek için {Fore.YELLOW}'Enter':{Fore.WHITE}  ")
            clear_screen()
            with open(dosya_yolu_4, "w") as dosya:
                dosya.write(a)
    def firma_adi_ile_fatura_ara(fatura_listesi, hedef_firma_adi):
        bulunan_faturalar = []
    
        for fatura in fatura_listesi:
            if hedef_firma_adi.lower() in fatura['Firma İsmi'].lower():
                bulunan_faturalar.append(fatura)
    
        return bulunan_faturalar
    
    def birden_cok_fatura_sil(fatura_listesi, secilen_indeksler, bulunan_faturalar):
        
        clear_screen()
        print(f"\n\n{Fore.YELLOW}Silinmesi{Fore.WHITE} İçin Seçilen Faturalar: ")
        gercek_indeksler = []

        for index in secilen_indeksler:
            fatura = bulunan_faturalar[index]
            logger.info(f"Seçilen Fatura: {index+1} - {fatura}")
            gercek_indeks = fatura_listesi.index(fatura)
            gercek_indeksler.append(gercek_indeks)

            if fatura['Durum'].startswith("Durum: [32mÖdendi"):
                renk=f"{Fore.GREEN}"
            else:
                renk=f"{Fore.RED}"
            print(f"\n  {Fore.YELLOW}{index+1}. Fatura {Fore.WHITE}\n\nTarih: {Fore.YELLOW}{fatura['Tarih']}{Fore.WHITE} \nFirma İsmi: {Fore.CYAN}{fatura['Firma İsmi']}{Fore.WHITE}\nFatura İçeriği: {fatura['Fatura İçeriği']}\nFatura Tutarı: {renk}{format_number(float(fatura['Fatura Tutarı'].split()[0]))} {Fore.WHITE}Türk Lirası {Fore.WHITE}\n{fatura['Durum']}\n")
            print("---------------------------------------------------------")
    
        
        print(f"\n\n\n{Fore.YELLOW}YUKARIDA SIRALANAN FATURALARI TEYİT ETTİKTEN SONRA SİLME İŞLEMİNİ ONAYLAYIN...{Fore.WHITE}")
        onay = input(f"\nSeçilen faturaları silmek istediğinizden emin misiniz? {Fore.YELLOW}(evet/hayır):{Fore.WHITE} ").lower()
        if onay == "evet" or onay == "e":
            gercek_indeksler.sort(reverse=True)
            for gercek_indeks in gercek_indeksler:
                del fatura_listesi[gercek_indeks]
                
            clear_screen()
            logger.info("Seçilen faturalar silindi.")
            print(f"\n\nFatura Silme işlemi {Fore.GREEN}BAŞARILI{Fore.WHITE} bir şekilde {Fore.YELLOW}TAMAMLANDI.{Fore.WHITE}")
            tm.sleep(1)
            print(f"\n\n{Fore.YELLOW}Sistemdeki Fatura Bilgileri Güncellendi.{Fore.WHITE}")
            bosluk()
            yukleniyor_cubugu(5)
            
    
        else:
            clear_screen()
            logger.info("Fatura silme işlemi iptal edildi.")
            print(f"\nFatura Silme işlemi {Fore.YELLOW}İPTAL EDİLDİ.{Fore.WHITE}")
            tm.sleep(1)
            print(f"\n\nSistemdeki Fatura Listesinde Herhangi Bir {Fore.YELLOW}DEĞİŞİKLİK YAPILMADI.{Fore.WHITE}")
            bosluk()
            yukleniyor_cubugu(5)
    
    def indeks_araligini_parse_et(indeks_araligi_str):
        indeksler = []
        try:
            
            if "-" in indeks_araligi_str:
                
                baslangic, bitis = map(int, indeks_araligi_str.split("-"))
                if baslangic > bitis:
                    clear_screen()
                    print(f"\n\nİlk Fatura Numarası İkinci Fatura'dan  {Fore.YELLOW}BÜYÜK OLAMAZ!!{Fore.WHITE} Lütfen geçerli Fatura numaraları girin.")
                    tm.sleep(5)
                    clear_screen()
                    ana_program_silme()
                indeksler.extend(range(baslangic - 1, bitis))
            else:
                for indeks_str in indeks_araligi_str.split():
                    if not indeks_str.isdigit():
                        print(f"\n\nFatura Numarası Sadece {Fore.YELLOW}RAKAMLARDAN OLUŞALABİLİR!{Fore.WHITE} Lütfen geçerli Fatura numaraları girin.")
                        tm.sleep(5)
                        clear_screen()
                        ana_program_silme()
                    indeksler.append(int(indeks_str) - 1)
        except ValueError:
            print(f"\n\nHatalı seçimler {Fore.YELLOW}İptal Ediliyor...{Fore.YELLOW}")
            tm.sleep(4)
            
    
        return indeksler
    
    def indeks_kontrol(secim,secilen,girilen):
        for indeks_str in secim.split():
            indeksler = indeks_araligini_parse_et(indeks_str)
        
            for indeks in indeksler:
                if indeks in girilen:
                    clear_screen()
                    print(f"\n\nAynı Fatura Numarası {Fore.YELLOW}İKİ KEZ GİRİLEMEZ!{Fore.WHITE}\n\n\nLütfen Geçerli Fatura Numaraları Seçin.")
                    tm.sleep(4)
                    clear_screen()
                    ana_program_silme()
                girilen.add(indeks)
        
            secilen.extend(indeksler)
        
       
        secilen.sort()
    def goruntule_invoices(fonk,title):
        logger.info(f"Faturalar listelendi. {title}")
        if not fonk:
            logger.info("Seçilen kriterlere göre fatura bulunamadı")
            print(f"\n\n\nSeçilen Kriterlere Ait Fatura {Fore.YELLOW}BULUNAMADI.{Fore.WHITE}")
            tm.sleep(3)
            tekrar_islem_silme()
            
            
            
        print(f"{title}")
        

        
        for index, invoice in enumerate(fonk, start=1):
            logger.info(f"{index} - {invoice}")
            if invoice['Durum'].startswith("Durum: [32mÖdendi"):
                renk = f"{Fore.GREEN}"
            else:
                renk = f"{Fore.RED}"
            
            print(f"\n  {Fore.YELLOW}{index}. Fatura {Fore.WHITE}\n\nTarih: {Fore.YELLOW}{invoice['Tarih']}{Fore.WHITE} \nFirma İsmi: {Fore.CYAN}{invoice['Firma İsmi']}{Fore.WHITE}\n\nFatura İçeriği: {invoice['Fatura İçeriği']}\n\nFatura Tutarı: {renk}{format_number(float(invoice['Fatura Tutarı'].split()[0]))} {Fore.WHITE}Türk Lirası {Fore.WHITE}\n{invoice['Durum']}\n")
            
            print("---------------------------------------------------------")
        
        while True:
            secilen_indeksler_str = input(f"\nSilmek istediğiniz {Fore.YELLOW}FATURALARI{Fore.WHITE} seçin (numaraları aralarında {Fore.YELLOW}BOŞLUK{Fore.WHITE} bırakarak veya {Fore.YELLOW}-{Fore.WHITE} aralık olarak belirtiniz. Örneğin(2 5 8-11): ")
            if secilen_indeksler_str == "":
                print(f"\n\n\n{Fore.YELLOW}Lütfen FATURA numarası giriniz.{Fore.WHITE}\n")
                tm.sleep(2)
                continue
            
            else:
                return secilen_indeksler_str,True 
    def tekrar_islem_silme():
        tekrar = input(f"\n\n\nYeniden başka bir işlem yapmak ister misiniz? {Fore.YELLOW}(Evet/Enter) {Fore.WHITE} | Ana Menü için {Fore.YELLOW}'Menu'{Fore.WHITE} : ").lower()
        
        tekrar_sorgu_silme_islemi(tekrar)
    def tekrar_islem_fatura_bulma():
        tekrar = input(f"\n\n\nYeniden başka bir işlem yapmak ister misiniz? {Fore.YELLOW}(Evet/Enter) {Fore.WHITE} | Ana Menü için {Fore.YELLOW}'Menu'{Fore.WHITE} : ").lower()
        
        fatura_bulma_tekrar_soru(tekrar)
        
        
    
    def fatura_liste(fonk,title):
        logger.info(f"Faturalar listelendi. {title}")
        if not fonk:
            logger.info("Seçilen kriterlere göre fatura bulunamadı.")
            print(f"\n\n\nSeçilen Kriterlere Ait Fatura {Fore.YELLOW}BULUNAMADI.{Fore.WHITE}")
            tm.sleep(3)
            tekrar_islem_fatura_bulma()
            
        print(f"{title}")

        for index, invoice in enumerate(fonk, start=1):
            logger.info(f"{index} - {invoice}")
            if invoice['Durum'].startswith("Durum: [32mÖdendi"):
                renk = f"{Fore.GREEN}"
            else:
                renk = f"{Fore.RED}"
            print(f"\n  {Fore.YELLOW}{index}. Fatura {Fore.WHITE}\n\nTarih: {Fore.YELLOW}{invoice['Tarih']}{Fore.WHITE} \nFirma İsmi: {Fore.CYAN}{invoice['Firma İsmi']}{Fore.WHITE}\n\nFatura İçeriği: {invoice['Fatura İçeriği']}\n\nFatura Tutarı: {renk}{format_number(float(invoice['Fatura Tutarı'].split()[0]))} {Fore.WHITE}Türk Lirası {Fore.WHITE}\n{invoice['Durum']}\n")
            print("---------------------------------------------------------")
    def sorgu_ekranı():
        logger.info("Sorgu ekranı sunuldu. ")
        print(f"\n                                                                                                              {Fore.YELLOW}Sorgu Seçenekleri:{Fore.WHITE}\n")
        print(f"\n                                                                                                              {Fore.YELLOW}0.{Fore.WHITE} Bu Sayfa Üzerinden DEVAM ET | Yeniden Arama")
        print(f"\n                                                                                                              {Fore.YELLOW}1.{Fore.WHITE} Tarih Aralığı ile Sorgula")
        print(f"\n                                                                                                              {Fore.YELLOW}2.{Fore.WHITE} Fatura Tutarı ile Sorgula")
        print(f"\n                                                                                                              {Fore.YELLOW}3.{Fore.WHITE} Her İkisini Beraber Sorgula")
        print(f"\n                                                                                                              {Fore.YELLOW}4.{Fore.WHITE} Çıkış")
    def fatura_bulma_tekrar_soru(soru):
        match soru:
            case "evet":
                logger.info("Fatura bulma yeniden başlatıldı.")
                yukleniyor_cubugu_3()
                clear_screen()
                main_fatura_bulma()
            case "menu":
                ana_menu()
            case _:
                logger.info("Program sonlandırıldı.")
                print("\n\nProgram sonlandırıldı.")
                tm.sleep(2)
                sys.exit()
    def check_existing_fatura(fatura_listesi, firma_ismi, tarih, icerik, tutar):
        for mevcut_fatura in fatura_listesi:
            benzerlik = 0
            if 'Firma İsmi' in mevcut_fatura and mevcut_fatura['Firma İsmi'].upper() == firma_ismi:
                benzerlik += 1
            if 'Fatura Tarihi' in mevcut_fatura and mevcut_fatura['Fatura Tarihi'] == tarih:
                benzerlik += 1
            if 'Fatura İçeriği' in mevcut_fatura and mevcut_fatura['Fatura İçeriği'] == icerik:
                benzerlik += 1
            if 'Fatura Tutarı' in mevcut_fatura and mevcut_fatura['Fatura Tutarı'] == tutar:
                benzerlik += 1
    
            benzerlik = benzerlik / 4
            if benzerlik >= 0.9:
                return True
        return False
    
    def main_fatura_bulma():
        logger.info("Fatura bulma açıldı.")
        invoice_list = []
    
        try:
            with open(dosya_yolu, "r", encoding="utf-8") as file:
                lines = file.readlines()
                i = 0
                while i < len(lines):
                    if i + 3 < len(lines) and lines[i].startswith("Firma ismi:"):
                        invoice = {
                            "Tarih": lines[i - 1].split(":")[1].strip(),
                            "Firma İsmi": lines[i].split(":")[1].strip(),
                            "Fatura İçeriği": lines[i + 1].split(":")[1].strip(),
                            "Fatura Tutarı": lines[i + 2].split(":")[1].strip(),
                            "Durum": lines[i + 3].strip()
                        }
                        invoice_list.append(invoice)
                    i += 1
        except FileNotFoundError:
            print(f"\n\n{Fore.RED}HATA:{Fore.WHITE} Fatura Listesi dosyası bulunamadı. Bilgilendirme için {Fore.YELLOW}LÜTFEN BEKLEYİNİZ...{Fore.WHITE}")
            tm.sleep(4)
        
        if invoice_list:
            clear_screen()
            print(f"\n\n        {Fore.YELLOW}FATURA BULMA UYGULAMASI{Fore.WHITE} ")
            print(f"""\n\n\n                                                                            {Fore.YELLOW}*{Fore.WHITE}Tüm Faturalar için {Fore.YELLOW}'Enter'{Fore.WHITE} basınız.""")
            target_name = input(f"\n\n\nFaturası aranacak {Fore.YELLOW}FİRMA{Fore.WHITE} ismini giriniz: ").upper()
            found_invoices = search_invoices_by_name(invoice_list, target_name)
            logger.info(f"Fatura Bulma için '{target_name}' araması yapıldı.")
            if found_invoices:
                
                clear_screen()
                print(f"\n{Fore.YELLOW}Faturalar bulundu:{Fore.WHITE} Firma ismi: {target_name}")
                logger.info("Fatura bulma için faturalar listelendi")
                for index, invoice in enumerate(found_invoices, start=1):
                    logger.info(f"{index} - {invoice}")
                    if invoice['Durum'].startswith("Durum: [32mÖdendi"):
                        renk=f"{Fore.GREEN}"
                    else:
                        renk=f"{Fore.RED}"
                    print(f"\n  {Fore.YELLOW}{index}. Fatura {Fore.WHITE}\n\nTarih: {Fore.YELLOW}{invoice['Tarih']}{Fore.WHITE} \nFirma İsmi: {Fore.CYAN}{invoice['Firma İsmi']}{Fore.WHITE}\n\nFatura İçeriği: {invoice['Fatura İçeriği']}\n\nFatura Tutarı: {renk}{format_number(float(invoice['Fatura Tutarı'].split()[0]))} {Fore.WHITE}Türk Lirası {Fore.WHITE}\n{invoice['Durum']}\n")
                    print("---------------------------------------------------------")
                
                sorgu_ekranı()
                while True:
                    choice = input(f"\n\n                                                                                                              {Fore.YELLOW}Seçiminizi yapın (0/1/2/3/4):{Fore.WHITE} ")
                    logger.info(f"Sorgu seçimi: {choice}")
                    match choice:
                        case "0":
                            break
                        case "1":
                            result=tarih_kontrol()
                            if result[-1]:
                                
                                start_datetime, end_datetime, success = result
        
                                filtered_invoices_by_date = filter_invoices_by_date(found_invoices, start_datetime, end_datetime)
                                clear_screen()
                                fatura_liste(filtered_invoices_by_date,f"\n{Fore.YELLOW}Tarih Aralığına{Fore.WHITE} Göre Arama Sonuçları:                    (Firma ismi: {target_name})")
                                break
                                
        
                                
                        case "2":
                            result=miktar_kontrol()
                            if result[-1]:
                                min_amount, max_amount, success = result
                                
                                filtered_invoices_by_amount = filter_invoices_by_amount(found_invoices, min_amount, max_amount)
                                clear_screen()
                                fatura_liste(filtered_invoices_by_amount,f"\n{Fore.YELLOW}Fatura Tutar Aralığına{Fore.WHITE} Göre Arama Sonuçları:                    (Firma ismi: {target_name})")
                                break
        
                              
                                
                        case "3":
                            
                            result=tarih_miktar_kontrol()
                            if result[-1]:
                                start_datetime, end_datetime, min_amount, max_amount, success = result
                                filtered_invoices_by_date = filter_invoices_by_date(found_invoices, start_datetime, end_datetime)
                                
                                
                                filtered_invoices_by_amount = filter_invoices_by_amount(filtered_invoices_by_date, min_amount, max_amount)
                                clear_screen()
                                fatura_liste(filtered_invoices_by_amount,f"\n{Fore.YELLOW}Tarih ve Tutar Aralığına{Fore.WHITE} Göre Arama Sonuçları:                   (Firma ismi: {target_name})")
                                break
                                
        
                        case "4":
                            clear_screen()
                            print("\n\nProgram sonlandırıldı.")
                            tm.sleep(2)
                            sys.exit()
                        case _:
                            
                            print(f"\n\n                                                                 {Fore.RED}GEÇERSİZ GİRİŞ!!!!{Fore.WHITE}")
                            tm.sleep(2)
                            continue
                    break
                                       
                    
                again = input(f"\n\n\nYeniden aramak ister misiniz? {Fore.YELLOW}(Evet/Hayır){Fore.WHITE}  | Ana Menü için {Fore.YELLOW}'Menu'{Fore.WHITE}: ").lower()
                fatura_bulma_tekrar_soru(again)

            else:
                logger.info(f"Aranılan isimle eşleşen fatura bulunmadı. '{target_name}'")
                print(f"\n\n\n\nAradığınız İsimle Eşleşen {Fore.YELLOW}FATURA BULUNAMADI.{Fore.WHITE}                    Firma ismi: {target_name}")
                again = input(f"\n\n\n\n\n\n\nYeniden aramak ister misiniz? {Fore.YELLOW}(Evet/Hayır){Fore.WHITE}    | Ana Menü için {Fore.YELLOW}'Menu'{Fore.WHITE}: ").lower()
                fatura_bulma_tekrar_soru(again)
        else:
            clear_screen()
            print(f"\n\nSistemde kayıtlı Fatura {Fore.YELLOW}BULUNMAMAKTADIR. {Fore.WHITE}Sisteme Fatura kayıt edildikten sonra tekrar deneyin. ")
            tm.sleep(7)
            sys.exit()
        logger.info("Fatura bulma işleminden çıkıldı.")
    
    def main_fatura_kaydetme():
        logger.info("Fatura kaydetme açıldı.")
        print(f"\n\n                                 {Fore.YELLOW}FATURA KAYDETME ARAYÜZÜ{Fore.WHITE}\n")
        print(f"""----------------------------------------------------------------------------------------
{Fore.YELLOW}*{Fore.WHITE}Kayıt esnasında hatalı bir yazım yapıldıysa program sonuna gelmeden programı kapatın.
    
    \n{Fore.YELLOW}-Oguzhan KUBAT{Fore.WHITE} tarafından oluşturulmuştur. Bilgisi dışında kullanımı yasaktır.     """)
    
        a = open(dosya_yolu, "a+", encoding="utf-8")
    
        fatura_listesi = []
    
        a.seek(0)
        lines = a.readlines()
        for i in range(0, len(lines), 6):
            firma_ismi = lines[i + 1].split(":")[1].strip()
            tarih = lines[i].split(":")[1].strip()
            icerik = lines[i + 2].split(":")[1].strip()
            tutar = float(lines[i + 3].split(":")[1].strip().split()[0])
            durum = lines[i + 4].split(":")[1].strip()
            fatura_listesi.append({
                'Firma İsmi': firma_ismi,
                'Fatura Tarihi': tarih,
                'Fatura İçeriği': icerik,
                'Fatura Tutarı': tutar,
                'Durum': durum
            })
        print("\n\n----------------------------------------------------------------------------------------")
        b = input(f"\n\n{Fore.YELLOW}Firma İsmi: {Fore.WHITE}").upper()
        c = input(f"\n{Fore.YELLOW}Fatura Tarihi giriniz (gg.aa.yyyy):{Fore.WHITE} ")
        try:
            c = datetime.strptime(c, "%d.%m.%Y")
        except ValueError:
            
            print(f"\n\n\n{Fore.RED}HATALI TARİH FORMATI!!  {Fore.YELLOW}31.12.9999 Şeklinde Tarih'i Belirtiniz!! {Fore.WHITE}")
            logger.info("Hatalı tarih formatı girildi.  Yeniden başlatılıyor...")
            tm.sleep(5)
            yukleniyor_cubugu_3()
            clear_screen()
            main_fatura_kaydetme()
    
        c = c.strftime("%d.%m.%Y")
        
        e = input(f"\n{Fore.YELLOW}Fatura İçeriğini giriniz:{Fore.WHITE} ")
        
        try:
            d = round(float(input(f"\n{Fore.YELLOW}Fatura Tutarını giriniz:{Fore.WHITE} ")), 2)
        except ValueError:
            print(
                f"\n\nFatura Tutarını {Fore.YELLOW}SAYI{Fore.WHITE} Olarak Giriniz! Küsürat İçin {Fore.YELLOW}Nokta{Fore.WHITE} Kullanınız.\n\n\n{Fore.YELLOW}LÜTFEN BEKLEYİNİZ...{Fore.WHITE}")
            logger.info("Hatalı tutar girildi.  Yeniden başlatılıyor...")
            tm.sleep(4)
            yukleniyor_cubugu_3()
            clear_screen()
            main_fatura_kaydetme()
    

    
        if check_existing_fatura(fatura_listesi, b, c, e, d):
            print(f"\n\nGirilen Bilgilerine Ait FATURA{Fore.YELLOW} SİSTEMDE MEVCUTTUR.{Fore.WHITE}")
            logger.info("Girilen bilgilere ait fatura sistemde mevcut. Yeniden başlatılıyor...")
            tm.sleep(2)
            print("\n\nLÜTFEN BEKLEYİNİZ...")
            tm.sleep(2)
            clear_screen()
            main_fatura_kaydetme()
        teyit_kaydetme=input(f"\n\nYukarıda Kayıt Edilecek {Fore.YELLOW}Fatura{Fore.WHITE} Bilgilerini Onaylıyor Musunuz? {Fore.YELLOW}Evet | Hayır :{Fore.WHITE} ").lower()
        match teyit_kaydetme:
            case "evet":
                pass
            case _:
                print("\n\n\nKayıt işlemi İptal Edilmiştir.")
                logger.info("Kayıt iptal edildi. Yeniden başlatılıyor...")
                yukleniyor_cubugu_3()
                clear_screen()
                main_fatura_kaydetme()
    
        a.write(f"Tarih: {c}\n")
        a.write(f"Firma ismi: {b}\n")
        a.write(f"Fatura içeriği: {e}\n")
        a.write(f"Fatura toplam tutar: {d} Türk Lirası\n")
        a.write(f"Durum: {Fore.YELLOW}Ödeme Bekliyor{Fore.WHITE}\n")
        a.write("---------------------------------------------------------\n")
        a.close()

        islem=input(f"""
    
Kayıt işlemi {Fore.GREEN}BAŞARILI{Fore.WHITE} bir şekilde {Fore.YELLOW}TAMAMLANMIŞTIR.{Fore.WHITE}
    


\n\nAna Menü için {Fore.YELLOW}'Menu'{Fore.WHITE} | Yeni Fatura Kayıt için {Fore.YELLOW}'Tekrar'{Fore.WHITE}  | Çıkış İçin {Fore.YELLOW}'Enter'{Fore.WHITE} :  """).lower()
        logger.info(f"Fatura kaydedildi. | {c} | {b} | {e} | {d}")
        match islem:
            case "menu":
                ana_menu()
            case "tekrar":
                yukleniyor_cubugu_3()
                clear_screen()
                logger.info()
                main_fatura_kaydetme()
            case _:
                logger.info("Programdan  sonlandırıldı.")
                sys.exit()
    def tekrar_sorgu_silme_islemi_2(soru):
        match soru:
            case "tekrar":
                yukleniyor_cubugu_3()
                ekran_temizle()
                ana_program_silme()
            case "menu":
                ana_menu()
            case _:

                print("\n\nProgram sonlandırıldı.")
                logger.info("Programdan sonlandırıldı.")
                tm.sleep(2)
                sys.exit()
    def tekrar_sorgu_silme_islemi(soru):
        match soru:
            case "evet":
                yukleniyor_cubugu_3()
                ekran_temizle()
                ana_program_silme()
            case "menu":
                ana_menu()
            case _:
                print("\n\nProgram sonlandırıldı.")
                logger.info("Programdan sonlandırıldı.")
                tm.sleep(2)
                sys.exit()
    def ana_program_silme():
        logger.info("Fatura Silme uygulaması açıldı.")
        fatura_listesi = []
    
        try:
            with open(dosya_yolu, "r", encoding="utf-8") as dosya:
                satirlar = dosya.readlines()
                i = 0
                while i < len(satirlar):
                    if i + 3 < len(satirlar) and satirlar[i].startswith("Firma ismi:"):
                        fatura = {
                            "Tarih": satirlar[i - 1].split(":")[1].strip(),
                            "Firma İsmi": satirlar[i].split(":")[1].strip(),
                            "Fatura İçeriği": satirlar[i + 1].split(":")[1].strip(),
                            "Fatura Tutarı": satirlar[i + 2].split(":")[1].strip(),
                            "Durum": satirlar[i + 3].strip()
                        }
                        fatura_listesi.append(fatura)
                    i += 1
        except FileNotFoundError:
            print(f"\n\n\n{Fore.RED}HATA: {Fore.WHITE}Fatura Listesi dosyası bulunamadı. Bilgilendirme için {Fore.YELLOW}LÜTFEN BEKLEYİNİZ...{Fore.WHITE}")
            tm.sleep(5)
    
        if fatura_listesi:
            ekran_temizle()
            print(f"\n\n{Fore.YELLOW}             FATURA SİLME UYGULAMASI")
            print(f"""\n\n\n                                                                            {Fore.YELLOW}*{Fore.WHITE}Tüm Faturalar için {Fore.YELLOW}'Enter'{Fore.WHITE} basınız.""")
            hedef_firma_adi = input(f"\n\nSilmek istediğiniz Faturanın {Fore.YELLOW}FİRMA{Fore.WHITE} ismini giriniz: ").upper()
            bulunan_faturalar = firma_adi_ile_fatura_ara(fatura_listesi, hedef_firma_adi)
            logger.info(f"Fatura silme için '{hedef_firma_adi}' araması yapıldı.")
            if bulunan_faturalar:
                logger.info("Fatura Silme için faturalar listelendi.")
                ekran_temizle()
                print(f"\nFaturalar bulundu:                     | Aranılan Firma ismi: {hedef_firma_adi.upper()}\n")
    
                for index, invoice in enumerate(bulunan_faturalar, start=1):
                    logger.info(f"{index}- {invoice}")
                    if invoice['Durum'].startswith("Durum: [32mÖdendi"):
                        renk=f"{Fore.GREEN}"
                    else:
                        renk=f"{Fore.RED}"
                    print(f"\n  {Fore.YELLOW}{index}. Fatura {Fore.WHITE}\n\nTarih: {Fore.YELLOW}{invoice['Tarih']}{Fore.WHITE} \nFirma İsmi: {Fore.CYAN}{invoice['Firma İsmi']}{Fore.WHITE}\n\nFatura İçeriği: {invoice['Fatura İçeriği']}\n\nFatura Tutarı: {renk}{format_number(float(invoice['Fatura Tutarı'].split()[0]))} {Fore.WHITE}Türk Lirası {Fore.WHITE}\n{invoice['Durum']}\n")
                    print("---------------------------------------------------------")
                sorgu_ekranı()
                secilen_indeksler = []
                girilen_indeksler = set()
                while True:
                    choice = input(f"\n\n                                                                                                              {Fore.YELLOW}Seçiminizi yapın (0/1/2/3/4):{Fore.WHITE} ")
                    logger.info(f"Sorgu seçimi: {choice}")
                    match choice:
                    
                        case "0":
                            while True:
                                
                                secilen_indeksler_str = input(f"\n\nSilmek istediğiniz {Fore.YELLOW}FATURALARI{Fore.WHITE} seçin (numaraları aralarında {Fore.YELLOW}BOŞLUK{Fore.WHITE} bırakarak veya {Fore.YELLOW}-{Fore.WHITE} aralık olarak belirtiniz. Örneğin(2 5 8-11): ")
                                logger.info(f"Seçilen indeksler: {secilen_indeksler_str}")
                                if secilen_indeksler_str=="":
                                    print(f"\n\n\n{Fore.YELLOW}Lütfen FATURA numarası giriniz.{Fore.WHITE}\n")
                                    tm.sleep(2)
                                    continue
                                break
                            
                            for indeks_str in secilen_indeksler_str.split():
                                indeksler = indeks_araligini_parse_et(indeks_str)
                            
                                for indeks in indeksler:
                                    if indeks in girilen_indeksler:
                                        print(f"\n\nAynı Fatura numarası {Fore.YELLOW}İKİ KEZ GİRİLEMEZ!{Fore.WHITE}\n\n\n{Fore.YELLOW}Lütfen geçerli Fatura numaraları seçin.{Fore.WHITE}")
                                        tm.sleep(5)
                                        ekran_temizle()
                                        ana_program_silme()
                                    girilen_indeksler.add(indeks)
                            
                                secilen_indeksler.extend(indeksler)
                            
                           
                            secilen_indeksler.sort()                            
                            
                            break
                                    
                        case "1":
                            result=tarih_kontrol()
                            if result[-1]:
                                start_datetime, end_datetime, success = result
                                filtered_invoices_by_date = filter_invoices_by_date(bulunan_faturalar, start_datetime, end_datetime)
                                bulunan_faturalar = filtered_invoices_by_date
                                ekran_temizle()
                                logger.info("Faturalar tarih aralığına göre listelendi.")
                                sonuc=goruntule_invoices(filtered_invoices_by_date,f"\n{Fore.YELLOW}Tarih Aralığına{Fore.WHITE} Göre Arama Sonuçları:")
                                
                                if sonuc[-1]:
                                    secilen_indeks_str,success=sonuc
                                    indeks_kontrol(secilen_indeks_str,secilen_indeksler,girilen_indeksler)
                                    break
                            break
                                
                        case "2":
                            result=miktar_kontrol()
                            if result[-1]:
                                min_amount, max_amount, success = result
                                filtered_invoices_by_amount = filter_invoices_by_amount(bulunan_faturalar, min_amount, max_amount)
                                bulunan_faturalar = filtered_invoices_by_amount
                                ekran_temizle()
                                logger.info("Faturalar tutar aralığına göre listelendi.")
                                sonuc=goruntule_invoices(filtered_invoices_by_amount,f"\n{Fore.YELLOW}Fatura Tutar Aralığına{Fore.WHITE} Göre Arama Sonuçları:")
                                
                                if sonuc[-1]:
                                    secilen_indeks_str,success=sonuc
                                    indeks_kontrol(secilen_indeks_str,secilen_indeksler,girilen_indeksler)
                                    break
                
                            break
                              
                        case "3":
                            result=tarih_miktar_kontrol()
                            if result[-1]:
                            
                                start_datetime, end_datetime, min_amount, max_amount, success = result
                                filtered_invoices_by_date = filter_invoices_by_date(bulunan_faturalar, start_datetime, end_datetime)
                                
                                
                                filtered_invoices_by_amount = filter_invoices_by_amount(filtered_invoices_by_date, min_amount, max_amount)
                                bulunan_faturalar = filtered_invoices_by_amount
                                ekran_temizle()
                                logger.info("Faturalar tarih ve tutar aralığına göre listelendi.")
                                sonuc=goruntule_invoices(filtered_invoices_by_amount,f"\n{Fore.YELLOW}Tarih ve Tutar Aralığına{Fore.WHITE} Göre Arama Sonuçları:")
                                
                                if sonuc[-1]:
                                    secilen_indeks_str,success=sonuc
                                    indeks_kontrol(secilen_indeks_str,secilen_indeksler,girilen_indeksler)
                                    break
        
                
                            break
                
                        case "4":
                            ekran_temizle()
                            print("\n\nProgram sonlandırıldı.")
                            logger.info("Program sonlandırıldı.")
                            tm.sleep(2)
                            sys.exit()
                        case _:
                            print(f"\n\n                                                                 {Fore.RED}GEÇERSİZ GİRİŞ!!!!{Fore.WHITE}")
                            tm.sleep(3)
                            continue
                    
                    logger.info("Fatura Silme işleminden çıkıldı.")
                    break
    

                if secilen_indeksler:
                    gecersiz_indeksler = [indeks for indeks in secilen_indeksler if indeks < 0 or indeks >= len(bulunan_faturalar)]
                    secilen_indeksler = [indeks for indeks in secilen_indeksler if indeks not in gecersiz_indeksler]
                    ekran_temizle()

                    if len(gecersiz_indeksler)>0 and  len(secilen_indeksler)==0:
                        pass
                    else:
                        birden_cok_fatura_sil(fatura_listesi, secilen_indeksler, bulunan_faturalar)
              
                        with open(dosya_yolu, "w", encoding="utf-8") as dosya:
                            for fatura in fatura_listesi:
                                dosya.write(f"Tarih: {fatura['Tarih']}\n")
                                dosya.write(f"Firma ismi: {fatura['Firma İsmi']}\n")
                                dosya.write(f"Fatura İçeriği: {fatura['Fatura İçeriği']}\n")
                                dosya.write(f"Fatura Tutarı: {fatura['Fatura Tutarı']}\n")
                                dosya.write(f"{fatura['Durum']}\n")
                                dosya.write("---------------------------------------------------------\n")
                    
                    if gecersiz_indeksler:
                        ekran_temizle()
                        if len(gecersiz_indeksler)>=0:
                            print(f"\n\nGeçersiz Fatura numaraları için {Fore.YELLOW}ÖDEME İŞLEMİ YAPILMAMIŞTIR.{Fore.WHITE}LÜTFEN BEKLEYİNİZ...")
                            print("\nGeçersiz fatura numaraları seçtiniz:", ", ".join(map(lambda x: str(x + 1), gecersiz_indeksler)))
                        tm.sleep(4)
                        clear_screen()
                        tekrar = input(f"\n\n\nSilme İşlemi {Fore.GREEN}Başarıyla{Fore.WHITE} Tamamlandı. Çıkış İçin {Fore.YELLOW}'Enter'{Fore.WHITE} | Yeniden Silme İşlemi İçin {Fore.YELLOW}'Tekrar'{Fore.WHITE}  | Ana Menü için {Fore.YELLOW}'Menu'{Fore.WHITE}: ").lower()
                        logger.info("Silme İşlemi tamamlandı.")
                        tekrar_sorgu_silme_islemi_2(tekrar)
                    ekran_temizle()
                    logger.info("Silme işlemi Tamamlandı.")
                    tekrar = input(f"\n\n\nSilme İşlemi {Fore.GREEN}Başarıyla{Fore.WHITE} Tamamlandı. Çıkış İçin {Fore.YELLOW}'Enter'{Fore.WHITE} | Yeniden Silme İşlemi İçin {Fore.YELLOW}'Tekrar'{Fore.WHITE}  | Ana Menü için {Fore.YELLOW}'Menu'{Fore.WHITE}: ").lower()
                    tekrar_sorgu_silme_islemi_2(tekrar)
            
            else:
                ekran_temizle()
                logger.info(f"Aranılan isimle eşlesen fatura bulunamadı. '{hedef_firma_adi}'")
                print(f"\n\n{Fore.YELLOW}Aradığınız isimle eşleşen Fatura Bulunamadı.{Fore.WHITE} |    Firma ismi: {hedef_firma_adi}")
                tm.sleep(4)
                tekrar_islem_silme()
        else:
            ekran_temizle()
            print(f"\n\nSistemde kayıtlı Fatura {Fore.YELLOW}BULUNMAMAKTADIR. {Fore.WHITE}Sisteme Fatura kayıt edildikten sonra tekrar deneyin. ")
            tm.sleep(7)
            sys.exit()
        
    def main():
        
        clear_screen()
    
    
        while True: 
            valid_indices = []
            invalid_indices = []
            invoice_list = []
    
            try:
                with open(dosya_yolu, "r+", encoding="utf-8") as file:
                    lines = file.readlines()
                    i = 0
                    while i < len(lines):
                        if i + 3 < len(lines) and lines[i].startswith("Firma ismi:"):
                            invoice = {
                                "Tarih": lines[i - 1].split(":")[1].strip(),
                                "Firma İsmi": lines[i].split(":")[1].strip(),
                                "Fatura İçeriği": lines[i + 1].split(":")[1].strip(),
                                "Fatura Tutarı": lines[i + 2].split(":")[1].strip(),
                                "Durum": lines[i + 3].strip()
                            }
                            invoice_list.append(invoice)
                        i += 1
            except FileNotFoundError:
                print(f"\n\n{Fore.RED}HATA: {Fore.WHITE}Fatura Listesi dosyası bulunamadı. Bilgilendirme için {Fore.YELLOW}LÜTFEN BEKLEYİNİZ...{Fore.WHITE}")
                tm.sleep(6)
    
            if invoice_list:
                clear_screen()
                logger.info("Fatura Ödeme Uygulaması açıldı.")
                print(f"""\n\n               {Fore.YELLOW}FATURA ÖDEME UYGULAMASI{Fore.WHITE}                                       | {Fore.YELLOW}BİLGİLENDİRME ***{Fore.WHITE} Yazıların Kayma Sorunu İçin {Fore.YELLOW}'*'{Fore.WHITE} basınız.
    
    
                                                                                         {Fore.YELLOW}*{Fore.WHITE}Tüm Faturalar için {Fore.YELLOW}'Enter'{Fore.WHITE} basınız.""")
                
                target_name = input(f"\n\n\nÖdemesini yapmak istediğiniz {Fore.YELLOW}Firmanın{Fore.WHITE} adını giriniz: ")
                logger.info(f"Fatura Ödeme uygulamasında '{target_name}' araması yapıldı.")
                if target_name.startswith("*"):
                    
                    bilgilendirme()
                    clear_screen()
                    continue
                
                found_invoices = search_invoices_by_name(invoice_list, target_name)
    
                if not found_invoices:
                    logger.info(f"Aranan fatura bulunamadı. '{target_name}'")
                    print(f"\n\n\n{Fore.YELLOW}'{target_name}'{Fore.WHITE} Adlı Firmaya ait Fatura BULUNAMADI!!")
                    tm.sleep(3)
                    bosluk()
                    yukleniyor_cubugu(3)
                    clear_screen()
                    continue
                else:
    
                    clear_screen()
    
                    print_invoices(found_invoices,f"{Fore.YELLOW}Arama Sonuçları:                {Fore.WHITE}| Firma adı: {target_name.upper()}",True)
                    sorgu_ekranı()
    
                    while True:
                        choice = input(f"\n\n                                                                                                              {Fore.YELLOW}Seçiminizi yapın (0/1/2/3/4):{Fore.WHITE} ")
                        logger.info(f"Sorgu seçimi: {choice}")
                        match choice:
                            
                            case "0":
                                print(f"\n                                                                                                        {Fore.WHITE}(Çıkış için: {Fore.YELLOW}'off'{Fore.WHITE} | Yeniden Arama için:{Fore.YELLOW} 'tekrar' {Fore.WHITE}) {Fore.CYAN}")
                                selected_indices = input(f"\n\nÖdeme yapmak istediğiniz Faturaların numaralarını aralarında {Fore.YELLOW}BOŞLUK{Fore.WHITE} bırakarak giriniz (ÖRNEĞİN: 5 7 11): ").split()
                                
                                select_kontrol(selected_indices)
    
                                indeks_sapta(selected_indices,found_invoices,valid_indices,invalid_indices)
                                break
    
                            case "1":
    
                                result=tarih_kontrol()
                                if result[-1]:
                                    start_datetime, end_datetime, success = result
                                    filtered_invoices_by_date = filter_invoices_by_date(found_invoices, start_datetime, end_datetime)
                                    found_invoices=filtered_invoices_by_date
                                    
                                    clear_screen()
    
                                    if not filtered_invoices_by_date:
                                        fatura_yok()
    
                                    print_invoices(filtered_invoices_by_date, f"{Fore.YELLOW}Tarih Aralığına{Fore.WHITE} Göre Arama Sonuçları:                   | Firma adı: {target_name.upper()}\n", True)
    
                                    print(f"\n                                                                                                        {Fore.WHITE}(Çıkış için: {Fore.YELLOW}'off'{Fore.WHITE} | Yeniden Arama için:{Fore.YELLOW} 'tekrar' {Fore.WHITE}) {Fore.CYAN}")                                                                                                        
                                    selected_indices = input(f"\n\nÖdeme yapmak istediğiniz Faturaların numaralarını aralarında {Fore.YELLOW}BOŞLUK{Fore.WHITE} bırakarak giriniz (ÖRNEĞİN: 5 7 11): ").split()                
                                    select_kontrol(selected_indices)
                                            
                                    indeks_sapta(selected_indices,filtered_invoices_by_date,valid_indices,invalid_indices)
                                        
                                    break
                            case "2":
    
                                result=miktar_kontrol()
                                if result[-1]:
                                    min_amount, max_amount, success = result
                                    filtered_invoices_by_amount = filter_invoices_by_amount(found_invoices, min_amount, max_amount)
                                    found_invoices=filtered_invoices_by_amount
                                    clear_screen()
                                    
                                    if not filtered_invoices_by_amount:
                                        fatura_yok()
                                        
                                    print_invoices(filtered_invoices_by_amount, f"{Fore.YELLOW}Tutar Aralığına{Fore.WHITE} Göre Arama Sonuçları:                   | Firma adı: {target_name.upper()}\n", True)
                                    print(f"\n                                                                                                        {Fore.WHITE}(Çıkış için: {Fore.YELLOW}'off'{Fore.WHITE} | Yeniden Arama için:{Fore.YELLOW} 'tekrar' {Fore.WHITE}) {Fore.CYAN}")                                                                                                        
                                    selected_indices = input(f"\n\nÖdeme yapmak istediğiniz Faturaların numaralarını aralarında {Fore.YELLOW}BOŞLUK{Fore.WHITE} bırakarak giriniz (ÖRNEĞİN: 5 7 11): ").split()                
                                       
                                    select_kontrol(selected_indices)
                                            
                                    indeks_sapta(selected_indices,filtered_invoices_by_amount,valid_indices,invalid_indices)
    
                                    break
    
                            case "3":
    
                                result=tarih_miktar_kontrol()
                                if result[-1]:
                                    start_datetime, end_datetime, min_amount, max_amount, success = result
                                    filtered_invoices_by_date = filter_invoices_by_date(found_invoices, start_datetime, end_datetime)
                                    
                                   
                                    filtered_invoices_by_amount = filter_invoices_by_amount(filtered_invoices_by_date, min_amount, max_amount)
                                    found_invoices=filtered_invoices_by_amount
                                    clear_screen()
                                    print()
                                    if not filtered_invoices_by_amount:
                                        fatura_yok()
    
                                    print_invoices(filtered_invoices_by_amount, f"{Fore.YELLOW}Tarih ve Tutar Aralığına{Fore.WHITE} Göre Arama Sonuçları:                  | Firma adı: {target_name.upper()}\n",True)
                                    
    
                                    print(f"\n                                                                                                        {Fore.WHITE}(Çıkış için: {Fore.YELLOW}'off'{Fore.WHITE} | Yeniden Arama için:{Fore.YELLOW} 'tekrar' {Fore.WHITE}) {Fore.CYAN}")                                                                                                        
                                    selected_indices = input(f"\n\nÖdeme yapmak istediğiniz Faturaların numaralarını aralarında {Fore.YELLOW}BOŞLUK{Fore.WHITE} bırakarak giriniz (ÖRNEĞİN: 5 7 11): ").split()                
                                    select_kontrol(selected_indices)
                                            
                                    indeks_sapta(selected_indices,filtered_invoices_by_amount,valid_indices,invalid_indices)
                                                    
                                    break
                            case "4":
    
                                clear_screen()
                                print("\n\nProgram sonlandırıldı.")
                                tm.sleep(2)
                                sys.exit()
                            case _:
                                print(f"\n\n                                                                 {Fore.RED}GEÇERSİZ GİRİŞ!!!!{Fore.WHITE}")
                                tm.sleep(2)
                                continue
                        break
                                  
            
                if valid_indices:
                    for index in valid_indices:
                        selected_invoice = found_invoices[index]
        
                        if selected_invoice['Durum'].startswith("Durum: [32mÖdendi"):
                            clear_screen()
                            
                            print(f"\n\n{Fore.CYAN}{selected_invoice['Firma İsmi']} {Fore.WHITE}Adlı Firmadan seçtiğiniz {Fore.YELLOW}{selected_invoice['Tarih']}{Fore.WHITE} tarihli {Fore.YELLOW}{format_number(float(selected_invoice['Fatura Tutarı'].split()[0]))} Türk Lirası {Fore.WHITE} tutarındaki FATURA önceden {Fore.GREEN}ÖDENMİŞ{Fore.WHITE}.\n\nSeçtiğiniz Faturalar arasında {Fore.RED}ÖDENMEMİŞ FATURALAR{Fore.WHITE} VAR İSE bilgileri kısa bir süre sonra aşağıdadır.")
                            bosluk()
                            yukleniyor_cubugu(7)
                            continue
                        clear_screen()
                        logger.info(f"Ödenmemiş fatura Teyit ekranına sunuldu. {index+1}- {selected_invoice}")
                        print(f"\n{Fore.YELLOW}-Ödenmemiş Fatura-\n\n\n\n{Fore.WHITE}{Fore.YELLOW}Tarih:{Fore.WHITE} {selected_invoice['Tarih']} \n\nFirma İsmi: {Fore.CYAN}{selected_invoice['Firma İsmi']}{Fore.WHITE} \n\n{Fore.YELLOW}Fatura Tutarı:{Fore.WHITE} {format_number(float(selected_invoice['Fatura Tutarı'].split()[0]))} Türk Lirası\n\n")
                        print(f"\n\n\n{Fore.YELLOW}TEYİT AMAÇLI FATURA BİLGİLERİNİZİ TEKRAR GİRİNİZ..")
                        tarih_input = input(f"\n\nFatura Tarihi Giriniz: {Fore.YELLOW}")
                        firma_input = input(f"\n{Fore.WHITE}Firma İsmi Giriniz (Küçük harfle giriniz!) : {Fore.YELLOW}").upper()
                        tutar_input = input(f"\n{Fore.WHITE}Faturanın Tutarını Giriniz (sadece sayı, virgül kullanmayınız! örneğin 10000.99) :  {Fore.YELLOW}")
    
        
                        
                        tutar = selected_invoice['Fatura Tutarı']
                        tutar_numeric = extract_number(tutar)
        
                        try:
                            tutar_input_numeric = float(tutar_input)
                            if tutar_input_numeric == tutar_numeric and tarih_input == selected_invoice['Tarih'] and firma_input == selected_invoice['Firma İsmi']:
                                tip_3=""
                                while True:
                                    tip=input(f"\n\n{Fore.WHITE}                                             Ödeme Tipini belirtiniz {Fore.YELLOW}(Nakit/Kart){Fore.WHITE}: ").capitalize()
                                    if "Kart" in tip :
                                        while True:
                                            tip_2_=input(f"\n\n\n                                                           Kartınızın {Fore.YELLOW}Banka{Fore.WHITE} Adı: ").title()
                                            if not tip_2_.isalpha() or tip_2_.isspace():
                                                print(f"\n\n                                                           Banka Adı Yalnızca {Fore.YELLOW}TEK KELİME{Fore.WHITE} İçerebilir.")
                                                tm.sleep(2)
                                                continue
                                            tip_2_ = re.sub(r'(bankası|banka)$', '', tip_2_)
                                            
                                            tip_2=input(f"\n\n\n                                                           Kartınızın {Fore.YELLOW}Son 4 Hanesi{Fore.WHITE}: ")
                                            tip_3=f"/{Fore.YELLOW} Sonu {tip_2} {Fore.WHITE}|{Fore.YELLOW} {tip_2_}{Fore.WHITE}"
                                            if tip_2.isdigit() and len(tip_2)==4:
                                                logger.info(f"Ödeme tipi 'Kart' Sonu {tip_2}| {tip_2_}")
                                                break
                                            else:
                                                print(f"\n\n                                                               {Fore.RED}GEÇERSİZ GİRİŞ!!!{Fore.WHITE}")
                                                tm.sleep(2)
                                                continue
                                            break
                                        break
                                            
                                    elif "Nakit" in tip:
                                        logger.info("Ödeme tipi 'Nakit'")
                                        tip_2=""
                                        
                                        break
                                    else:
                                        
                                        print(f"\n\n                                                             Lütfen {Fore.YELLOW}ÖDEME TİPİNİ{Fore.WHITE} doğru seçiniz!!")
                                        tm.sleep(2)
                                        continue
                                logger.info("Teyit Onaylandı.")
                                now = datetime.now()
                                formatted_time = now.strftime("   %H:%M:%S")
                                formatted_zaman=now.strftime("%d.%m.%Y")
                                selected_invoice['Durum'] = f"Durum: {Fore.GREEN}Ödendi{Fore.WHITE} ---------- {Fore.YELLOW}{tip}{Fore.WHITE} {tip_3}  [{formatted_zaman}]{formatted_time}"
                                logger.info(f"Ödemesi Gerçekleşen Fatura: {selected_invoice}")
                                
                                with open(dosya_yolu, "w", encoding="utf-8") as file:
                                    
                                    for invoice in invoice_list:
                                        
                                        file.write(f"Tarih: {invoice['Tarih']}\n")
                                        file.write(f"Firma ismi: {invoice['Firma İsmi']}\n")
                                        file.write(f"Fatura içeriği: {invoice['Fatura İçeriği']}\n")
                                        file.write(f"Fatura toplam tutar: {invoice['Fatura Tutarı']}\n")
                                        file.write(f"{invoice['Durum']}\n")
                                        file.write("---------------------------------------------------------\n")
                                        
                                clear_screen()
                                print(f"\n\n\n{Fore.CYAN}{selected_invoice['Firma İsmi'].upper()}{Fore.WHITE} Adlı Firmanın {Fore.YELLOW}{selected_invoice['Tarih']}{Fore.WHITE} tarihli {Fore.YELLOW}{format_number(float(selected_invoice['Fatura Tutarı'].split()[0]))} Türk Lirası {Fore.WHITE}tutarındaki Faturası {Fore.GREEN}BAŞARILI{Fore.WHITE} bir şekilde {Fore.YELLOW}ÖDENDİ{Fore.WHITE} olarak {Fore.YELLOW}SİSTEM'E{Fore.WHITE} Kayıt Edildi.\n\n")
                                bosluk()
                                yukleniyor_cubugu(5)
                                
                            else:
                                clear_screen()
                                logger.info(f"Teyit Bilgileri uyuşmadı. {selected_invoice}")
                                print(f"\n\n{Fore.WHITE}Girilen bilgiler {Fore.YELLOW}Sistemdeki{Fore.WHITE} FATURA Bilgileriyle Uyuşmadığından İşleminize {Fore.YELLOW}DEVAM EDİLEMEMEKTEDİR.{Fore.WHITE}")
                                v=str(input(f"\n\n\nÖdeme İşlemini Tekrar Denemek İçin {Fore.YELLOW}'Evet'{Fore.WHITE}, Diğer Faturalar ile DEVAM Etmek için {Fore.YELLOW}'Enter'{Fore.WHITE} basınız:  ")).lower()
                                if v == "evet" or v == "e":
                                    for i, invoice in enumerate(found_invoices):
                                        if invoice == selected_invoice:
                                            
                                            index = i
                                            break
                                    
                                    clear_screen()
                                    bosluk()
                                    yukleniyor_cubugu(2)
                                    valid_indices.append(index)
                                    valid_indices.sort()
                                        
                                else:
                                    clear_screen()
                                    print(f"\n\n\n{Fore.YELLOW}Ödeme işlemi{Fore.WHITE}, Mevcut ise sıradaki Faturalar için {Fore.YELLOW}DEVAM EDECEKTİR.{Fore.WHITE}")
                                    bosluk()
                                    yukleniyor_cubugu(3)
                        except ValueError:
                            clear_screen()
                            logger.info(f"Teyit Bilgileri uyuşmadı. {selected_invoice}")
                            print(f"\n\n{Fore.WHITE}Girilen Bilgiler {Fore.YELLOW}Sistemdeki{Fore.WHITE} Fatura Bilgileriyle Uyuşmadığından İşleminize {Fore.YELLOW}DEVAM EDİLEMEMEKTEDİR.{Fore.WHITE}")
                            v=str(input(f"\n\n\nÖdeme İşlemini Tekrar Denemek İçin {Fore.YELLOW}'Evet'{Fore.WHITE}, Diğer Faturalar ile DEVAM ETMEK için {Fore.YELLOW}'Enter'{Fore.WHITE} basınız:  ")).lower()
                            if v == "evet" or v == "e":
                                for i, invoice in enumerate(found_invoices):
                                    if invoice == selected_invoice:
                                            
                                        index = i
                                        break
                                    
                                clear_screen()
                                bosluk()
                                yukleniyor_cubugu(2)
                                valid_indices.append(index)
                                valid_indices.sort()
    
                            else:
                                clear_screen()
                                print(f"\n\n\n{Fore.YELLOW}Ödeme işlemi{Fore.WHITE}, Mevcut ise sıradaki Faturalar için {Fore.YELLOW}DEVAM EDECEKTİR.{Fore.WHITE}")
                                bosluk()
                                yukleniyor_cubugu(3)
        
                if invalid_indices and "tekrar" not in invalid_indices:
                    invalid_indices = [x for x in invalid_indices if x.strip()]
                                
                    clear_screen()
                    print(f"\n\n{Fore.WHITE}Geçersiz Fatura Numaraları:", ", ".join(invalid_indices))
                    print(f"\n\n{Fore.WHITE}Girilen Geçersiz Fatura Numaraları için {Fore.YELLOW}ÖDEME İŞLEMİ YAPILMAMIŞTIR.{Fore.WHITE}")
                    bosluk()
                    yukleniyor_cubugu(5)
                clear_screen()
                logger.info("Ödeme işlemi Tamamlandı.")
                n = input(f"\n\n\n{Fore.YELLOW}Ödeme İşlemi{Fore.WHITE} Başarıyla {Fore.GREEN}TAMAMLANDI.{Fore.WHITE} Programı Kapatmak İçin {Fore.YELLOW}'Enter'{Fore.WHITE} basınız | Yeniden Arama için {Fore.YELLOW}'Tekrar'{Fore.WHITE} | Ana Menü için {Fore.YELLOW}'Menu' {Fore.WHITE} yazınız: ").lower()
                match n:
                    case "tekrar":
                        clear_screen()
                        bosluk()
                        yukleniyor_cubugu(2)
                        clear_screen()
                        continue
                    case "menu":
                        ana_menu()
                    case "":
                        
                        sys.exit()
                    case _:
                        print("\n\nGEÇERSİZ GİRİŞ.")
                        print("\n\nProgram 3 sn içinde kapanacaktır...")
                        tm.sleep(3)
                        sys.exit()
              
            else:
                clear_screen()
                print(f"\n\nSistemde kayıtlı Fatura {Fore.YELLOW}BULUNMAMAKTADIR. {Fore.WHITE}Sisteme Fatura kayıt edildikten sonra tekrar deneyin. ")
                tm.sleep(5)
                sys.exit()
except Exception as hata:
    clear_screen()
    print("\n\nHay aksii!! Bir problem oluştu.")
    hata_kaydet(str(hata))
    tm.sleep(2)
    print("\n\nHata teknik ekibe iletildi. En kısa sürede çözülecektir.")
    input(f"\n\nÇıkış için {Fore.YELLOW}Enter: ")
    sys.exit()
            
if __name__ == "__main__":
    giris()

    










