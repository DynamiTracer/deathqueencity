from django.db import models

class History(models.Model):
    History_Date = models.CharField(max_length=250)
    History_Text = models.CharField(max_length=250)
    Delete_Flg = models.IntegerField(default=0)

    def __str__(self):
        return self.History_Date

class SearchData(models.Model):
    Provider = models.CharField(max_length=250)
    SearchName = models.CharField(max_length=250)
    InsertDate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.History_Date

class Wanted(models.Model):
    Genre = models.CharField(max_length=250)
    Soft_Title = models.CharField(max_length=250)
    Goods_Detail = models.CharField(max_length=250)
    Price = models.CharField(max_length=250)
    Delete_Flg = models.IntegerField(default=0)

    def __str__(self):
        return self.Goods_Detail

class Category(models.Model):
    Category_ID = models.CharField(max_length=4)
    Category_Name = models.CharField(max_length=250)
    Category_Group = models.CharField(max_length=250)
    Category_Key = models.CharField(max_length=250)
    Category_GroupID = models.CharField(max_length=250)
    Delete_Flg = models.IntegerField(default=0)
    def __str__(self):
        return self.Category_Name
        
class Soft(models.Model):
    Media = models.CharField(max_length=250)
    Soft_ID = models.CharField(max_length=4)
    Classification = models.CharField(max_length=250)
    Soft_Keyname = models.CharField(max_length=250)
    Soft_Name_Short = models.CharField(max_length=250)
    Soft_Name = models.CharField(max_length=250)
    Soft_Name_Kana = models.CharField(max_length=250)
    Soft_Group = models.CharField(max_length=250)
    Release_Date = models.CharField(max_length=250)
    Price = models.CharField(max_length=250)
    Genre = models.CharField(max_length=250)
    Standard_Number = models.CharField(max_length=250)
    def __str__(self):
        return self.Soft_Name

class Item(models.Model):
    Category_key = models.CharField(max_length=100)
    Item_Classification = models.CharField(max_length=250)
    Sort_No = models.CharField(max_length=250)
    Preface = models.CharField(max_length=250)
    Comment = models.CharField(max_length=250)
    Image_ID= models.CharField(max_length=4)
    Rare = models.CharField(max_length=1)
    Insert_Date = models.CharField(max_length=250)
    Soft_Keyname1 = models.CharField(max_length=250)
    Thumbnail1 = models.CharField(max_length=250)
    Picpath1 = models.CharField(max_length=250)
    Alt1 = models.CharField(max_length=250)
    Soft_Keyname2 = models.CharField(max_length=250)
    Thumbnail2 = models.CharField(max_length=250)
    Picpath2 = models.CharField(max_length=250)
    Alt2 = models.CharField(max_length=250)
    Soft_Keyname3 = models.CharField(max_length=250)
    Thumbnail3 = models.CharField(max_length=250)
    Picpath3 = models.CharField(max_length=250)
    Alt3 = models.CharField(max_length=250)
    Soft_Keyname4 = models.CharField(max_length=250)
    Thumbnail4 = models.CharField(max_length=250)
    Picpath4 = models.CharField(max_length=250)
    Alt4 = models.CharField(max_length=250)
    Soft_Keyname5 = models.CharField(max_length=250)
    Thumbnail5 = models.CharField(max_length=250)
    Picpath5 = models.CharField(max_length=250)
    Alt5 = models.CharField(max_length=250)
    Soft_Keyname6 = models.CharField(max_length=250)
    Thumbnail6 = models.CharField(max_length=250)
    Picpath6 = models.CharField(max_length=250)
    Alt6 = models.CharField(max_length=250)
    Soft_Keyname7 = models.CharField(max_length=250)
    Thumbnail7 = models.CharField(max_length=250)
    Picpath7 = models.CharField(max_length=250)
    Alt7 = models.CharField(max_length=250)
    Soft_Keyname8 = models.CharField(max_length=250)
    Thumbnail8 = models.CharField(max_length=250)
    Picpath8 = models.CharField(max_length=250)
    Alt8 = models.CharField(max_length=250)

    def __str__(self):
        return self.Picpath1

class Image(models.Model):
    Soft_Keyname = models.CharField(max_length=250)
    Category_Key = models.CharField(max_length=4)    
    Image_ID = models.CharField(max_length=4)
    Thumbnail = models.CharField(max_length=250)
    Picpath = models.CharField(max_length=250)
    Alt = models.CharField(max_length=250)
    def __str__(self):
        return self.Name
