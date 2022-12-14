from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from .models import Soft, History, Wanted, Category, Item, Image, SearchData
from django.views import View
import random

class MyView(View):
    def get(self, request):
        # 'HTTP_X_FORWARDED_FOR'ヘッダを参照して転送経路のIPアドレスを取得する。
        forwarded_addresses = request.META.get('HTTP_X_FORWARDED_FOR')
        if forwarded_addresses:
            # 'HTTP_X_FORWARDED_FOR'ヘッダがある場合: 転送経路の先頭要素を取得する。
            client_addr = forwarded_addresses.split(',')[0]
        else:
            # 'HTTP_X_FORWARDED_FOR'ヘッダがない場合: 直接接続なので'REMOTE_ADDR'ヘッダを参照する。
            client_addr = request.META.get('REMOTE_ADDR')

        # 動作確認のため、取得したアドレスをそのまま返す。
        return HttpResponse(client_addr)

class IndexView(ListView):
    template_name = 'index.html'
    context_object_name = 'soft_list'
    model = Soft

    
    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)

        SearchData(Provider=self.request._current_scheme_host, SearchName="index" ).save()

#        q=AccessCount.objects.values(AccessCount)
#        kaisuu=q.access_no+1
#        q.access_no=kaisuu
#        q.save()
#        textCount = 'count : ' + str(kaisuu) 
        
#        context['AccessCount'] = textCount



        context.update({
            'category_list': Category.objects.all().filter(Delete_Flg='0').order_by('id'),
        })

        context['FileName'] = 'Home'
        context['GoodsPic'] = random.randrange(10)

        return context
        
    def get_queryset(self):
        return Soft.objects.all().filter(Classification='1').order_by('id')

class QueenView(ListView):
    template_name = 'queen.html'
    context_object_name = 'soft_list'
    model = SearchData

    def get_context_data(self, **kwargs):
        context = super(QueenView, self).get_context_data(**kwargs)

        context.update({
            'category_list': Category.objects.all().filter(Delete_Flg='0').order_by('id'),            
            'searchdata_list': SearchData.objects.all().order_by('-id')[:1000],
        })

        context['FileName'] = 'Queen'

        return context

    def get_queryset(self):
        return Soft.objects.all().filter(Classification='1').order_by('id')

class SpecialView(ListView):
    template_name = 'special.html'
    context_object_name = 'soft_list'
    model = Soft

    def get_context_data(self, **kwargs):
        context = super(SpecialView, self).get_context_data(**kwargs)
        pk = self.kwargs['pk']
        context.update({
            'category_list': Category.objects.all().filter(Delete_Flg='0').order_by('id'),
        })

        if pk == 1:        
            context['FileName'] = 'Special1'
            SearchData(Provider=self.request._current_scheme_host, SearchName="Special1").save()        

        elif pk == 2:
            context['FileName'] = 'Special2'
            SearchData(Provider=self.request._current_scheme_host, SearchName="Special2").save()        

        return context

    def get_queryset(self):
        return Soft.objects.all().filter(Classification='1').order_by('id')

#Soft
class SoftView(ListView):
    template_name = 'soft.html'
    context_object_name = 'soft_list'
    model = Soft

    def get_context_data(self, **kwargs):

        context = super(SoftView, self).get_context_data(**kwargs)
        pk = self.kwargs['pk']

        sql =   'SELECT * FROM ( SELECT '
        sql +=  'A1.id as id, '
        sql +=  'A1.Sort_no as Sort_no, '
        sql +=  'A1.Preface as Preface,'
        sql +=  'A1.Comment as Comment, '
        sql +=  'A1.Image_ID as Image_ID, '
        sql +=  'A1.Picpath1 as Picpath, '
        sql +=  'A1.Item_Classification as ItemC, '
        sql +=  'A1.Thumbnail1 as Thumb, '
        sql +=  'A1.Alt1 as Alt, '
        sql +=  'B1.Soft_ID as Soft_ID, '
        sql +=  'B1.Soft_Keyname as Soft_Keyname, '
        sql +=  'B1.Soft_Name_Short as Soft_Name_Short, '
        sql +=  'B1.Soft_Name as Soft_Name, '
        sql +=  'CASE Category_Name WHEN "テレホンカード 1987-1996" THEN "テレホンカード" '
        sql +=  'WHEN "テレホンカード 1997-1998" THEN "テレホンカード" '
        sql +=  'WHEN "テレホンカード 1999-2002" THEN "テレホンカード" '
        sql +=  'WHEN "FFⅤカードコレクションズ" THEN "カードコレクションズ" ' 
        sql +=  'WHEN "クロノトリガー プリズムカード" THEN "プリズムカード" '
        sql +=  'WHEN "ファミコンスナック FFⅡ PART1" THEN "ファミコンスナック PART1" '        
        sql +=  'WHEN "ファミコンスナック FFⅡ PART2" THEN "ファミコンスナック PART2" '
        sql +=  'WHEN "FFⅥカードダス PART1" THEN "カードダス PART1" ' 
        sql +=  'WHEN "FFⅥカードダス PART2" THEN "カードダス PART2" '        
        sql +=  'WHEN "PC88・98・FM-7・X1・MSX" THEN "" '
        sql +=  'WHEN "ファミコン・ディスクシステム" THEN "" '        
        sql +=  'WHEN "ゲームボーイ" THEN "" '
        sql +=  'WHEN "スーパーファミコン" THEN "" '        
        sql +=  'WHEN "付録 FC・FCD・GB" THEN "付録" '
        sql +=  'WHEN "付録 SFC" THEN "付録" '
        sql +=  'WHEN "攻略本 FC・FCD・GB" THEN "攻略本" '
        sql +=  'WHEN "攻略本 SFC" THEN "攻略本" '
        sql +=  'WHEN "マリオＲＰＧ トップサンシール" THEN "トップサンシール" '
        sql +=  'ELSE Category_Name '
        sql +=  'END Category_Name, '
        sql +=  'CASE WHEN C1.Category_ID = "101" AND B1.Soft_Name = "キングスナイト" THEN "102" '
        sql +=  'WHEN C1.Category_ID = "101" AND B1.Soft_Name = "テグザー" THEN "102" '
        sql +=  'WHEN C1.Category_ID = "101" AND B1.Soft_Name = "ファイナルファンタジー" THEN "102" '
        sql +=  'ELSE C1.Category_ID '
        sql +=  'END Category_ID, '
        sql +=  'C1.Category_Group as Category_Group '
        sql +=  'FROM dqc_item as A1 '
        sql +=  'INNER JOIN dqc_soft as B1 '
        sql +=  'on A1.Soft_Keyname1 = B1.Soft_Keyname '
        sql +=  'LEFT JOIN dqc_category as C1 '
        sql +=  'on A1.Category_key = C1.Category_Key '        

        sql +=  'union '

        sql +=  'SELECT '
        sql +=  'A2.id as id, '
        sql +=  'A2.Sort_no as Sort_no, '
        sql +=  'A2.Preface as Preface,'
        sql +=  'A2.Comment as Comment, '
        sql +=  'A2.Image_ID as Image_ID, '
        sql +=  'A2.Picpath2 as Picpath, '
        sql +=  'A2.Item_Classification as ItemC, '
        sql +=  'A2.Thumbnail2 as Thumb, '
        sql +=  'A2.Alt2 as Alt, '
        sql +=  'B2.Soft_ID as Soft_ID, '
        sql +=  'B2.Soft_Keyname as Soft_Keyname, '
        sql +=  'B2.Soft_Name_Short as Soft_Name_Short, '
        sql +=  'B2.Soft_Name as Soft_Name, '
        sql +=  'CASE Category_Name WHEN "テレホンカード 1987-1996" THEN "テレホンカード" '
        sql +=  'WHEN "テレホンカード 1997-1998" THEN "テレホンカード" '
        sql +=  'WHEN "テレホンカード 1999-2002" THEN "テレホンカード" '
        sql +=  'WHEN "クロノトリガー プリズムカード" THEN "プリズムカード" '
        sql +=  'WHEN "FFⅤカードコレクションズ" THEN "カードコレクションズ" ' 
        sql +=  'WHEN "ファミコンスナック FFⅡ PART1" THEN "ファミコンスナック PART1" '        
        sql +=  'WHEN "ファミコンスナック FFⅡ PART2" THEN "ファミコンスナック PART2" '
        sql +=  'WHEN "FFⅥカードダス PART1" THEN "カードダス PART1" ' 
        sql +=  'WHEN "FFⅥカードダス PART2" THEN "カードダス PART2" '        
        sql +=  'WHEN "PC88・98・FM-7・X1・MSX" THEN "" '
        sql +=  'WHEN "ファミコン・ディスクシステム" THEN "" '        
        sql +=  'WHEN "ゲームボーイ" THEN "" '
        sql +=  'WHEN "スーパーファミコン" THEN "" '        
        sql +=  'WHEN "付録 FC・FCD・GB" THEN "付録" '
        sql +=  'WHEN "付録 SFC" THEN "付録" '
        sql +=  'WHEN "攻略本 FC・FCD・GB" THEN "攻略本" '
        sql +=  'WHEN "攻略本 SFC" THEN "攻略本" '
        sql +=  'WHEN "マリオＲＰＧ トップサンシール" THEN "トップサンシール" '
        sql +=  'ELSE Category_Name '
        sql +=  'END Category_Name, '
        sql +=  'CASE WHEN C2.Category_ID = "101" AND B2.Soft_Name = "キングスナイト" THEN C2.Category_ID = "102" '
        sql +=  'WHEN C2.Category_ID = "101" AND B2.Soft_Name = "テグザー" THEN C2.Category_ID = "102" '
        sql +=  'WHEN C2.Category_ID = "101" AND B2.Soft_Name = "ファイナルファンタジー" THEN C2.Category_ID = "102" '
        sql +=  'ELSE C2.Category_ID '
        sql +=  'END Category_ID, '
        sql +=  'C2.Category_Group as Category_Group '        
        sql +=  'FROM dqc_item as A2 '
        sql +=  'INNER JOIN dqc_soft as B2 '
        sql +=  'on A2.Soft_Keyname2 = B2.Soft_Keyname '
        sql +=  'LEFT JOIN dqc_category as C2 '
        sql +=  'on A2.Category_key = C2.Category_Key '        

        sql +=  'union '

        sql +=  'SELECT '
        sql +=  'A3.id as id, '
        sql +=  'A3.Sort_no as Sort_no, '
        sql +=  'A3.Preface as Preface,'
        sql +=  'A3.Comment as Comment, '
        sql +=  'A3.Image_ID as Image_ID, '
        sql +=  'A3.Picpath3 as Picpath, '
        sql +=  'A3.Item_Classification as ItemC, '
        sql +=  'A3.Thumbnail3 as Thumb, '
        sql +=  'A3.Alt3 as Alt, '        
        sql +=  'B3.Soft_ID as Soft_ID, '
        sql +=  'B3.Soft_Keyname as Soft_Keyname, '
        sql +=  'B3.Soft_Name_Short as Soft_Name_Short, '
        sql +=  'B3.Soft_Name as Soft_Name, '
        sql +=  'CASE Category_Name WHEN "テレホンカード 1987-1996" THEN "テレホンカード" '
        sql +=  'WHEN "テレホンカード 1997-1998" THEN "テレホンカード" '
        sql +=  'WHEN "テレホンカード 1999-2002" THEN "テレホンカード" '
        sql +=  'WHEN "クロノトリガー プリズムカード" THEN "プリズムカード" '
        sql +=  'WHEN "FFⅤカードコレクションズ" THEN "カードコレクションズ" ' 
        sql +=  'WHEN "ファミコンスナック FFⅡ PART1" THEN "ファミコンスナック PART1" '        
        sql +=  'WHEN "ファミコンスナック FFⅡ PART2" THEN "ファミコンスナック PART2" '
        sql +=  'WHEN "FFⅥカードダス PART1" THEN "カードダス PART1" ' 
        sql +=  'WHEN "FFⅥカードダス PART2" THEN "カードダス PART2" '        
        sql +=  'WHEN "PC88・98・FM-7・X1・MSX" THEN "" '
        sql +=  'WHEN "ファミコン・ディスクシステム" THEN "" '        
        sql +=  'WHEN "ゲームボーイ" THEN "" '
        sql +=  'WHEN "スーパーファミコン" THEN "" '        
        sql +=  'WHEN "付録 FC・FCD・GB" THEN "付録" '
        sql +=  'WHEN "付録 SFC" THEN "付録" '
        sql +=  'WHEN "攻略本 FC・FCD・GB" THEN "攻略本" '
        sql +=  'WHEN "攻略本 SFC" THEN "攻略本" '
        sql +=  'WHEN "マリオＲＰＧ トップサンシール" THEN "トップサンシール" '
        sql +=  'ELSE Category_Name '
        sql +=  'END Category_Name, '
        sql +=  'CASE WHEN C3.Category_ID = "101" AND B3.Soft_Name = "キングスナイト" THEN "102" '
        sql +=  'WHEN C3.Category_ID = "101" AND B3.Soft_Name = "テグザー" THEN "102" '
        sql +=  'WHEN C3.Category_ID = "101" AND B3.Soft_Name = "ファイナルファンタジー" THEN "102" '
        sql +=  'ELSE C3.Category_ID '
        sql +=  'END Category_ID, '
        sql +=  'C3.Category_Group as Category_Group '        
        sql +=  'FROM dqc_item as A3 '
        sql +=  'INNER JOIN dqc_soft as B3 '
        sql +=  'on A3.Soft_Keyname3 = B3.Soft_Keyname '
        sql +=  'LEFT JOIN dqc_category as C3 '
        sql +=  'on A3.Category_key = C3.Category_Key '        

        sql +=  'union '

        sql +=  'SELECT '
        sql +=  'A4.id as id, '
        sql +=  'A4.Sort_no as Sort_no, '
        sql +=  'A4.Preface as Preface,'
        sql +=  'A4.Comment as Comment, '
        sql +=  'A4.Image_ID as Image_ID, '
        sql +=  'A4.Picpath4 as Picpath, '
        sql +=  'A4.Item_Classification as ItemC, '
        sql +=  'A4.Thumbnail4 as Thumb, '
        sql +=  'A4.Alt4 as Alt, '                
        sql +=  'B4.Soft_ID as Soft_ID, '
        sql +=  'B4.Soft_Keyname as Soft_Keyname, '
        sql +=  'B4.Soft_Name_Short as Soft_Name_Short, '
        sql +=  'B4.Soft_Name as Soft_Name, '
        sql +=  'CASE Category_Name WHEN "テレホンカード 1987-1996" THEN "テレホンカード" '
        sql +=  'WHEN "テレホンカード 1997-1998" THEN "テレホンカード" '
        sql +=  'WHEN "テレホンカード 1999-2002" THEN "テレホンカード" '
        sql +=  'WHEN "クロノトリガー プリズムカード" THEN "プリズムカード" '
        sql +=  'WHEN "FFⅤカードコレクションズ" THEN "カードコレクションズ" ' 
        sql +=  'WHEN "ファミコンスナック FFⅡ PART1" THEN "ファミコンスナック PART1" '        
        sql +=  'WHEN "ファミコンスナック FFⅡ PART2" THEN "ファミコンスナック PART2" '
        sql +=  'WHEN "FFⅥカードダス PART1" THEN "カードダス PART1" ' 
        sql +=  'WHEN "FFⅥカードダス PART2" THEN "カードダス PART2" '        
        sql +=  'WHEN "PC88・98・FM-7・X1・MSX" THEN "" '
        sql +=  'WHEN "ファミコン・ディスクシステム" THEN "" '        
        sql +=  'WHEN "ゲームボーイ" THEN "" '
        sql +=  'WHEN "スーパーファミコン" THEN "" '        
        sql +=  'WHEN "付録 FC・FCD・GB" THEN "付録" '
        sql +=  'WHEN "付録 SFC" THEN "付録" '
        sql +=  'WHEN "攻略本 FC・FCD・GB" THEN "攻略本" '
        sql +=  'WHEN "攻略本 SFC" THEN "攻略本" '
        sql +=  'WHEN "マリオＲＰＧ トップサンシール" THEN "トップサンシール" '
        sql +=  'ELSE Category_Name '
        sql +=  'END Category_Name, '
        sql +=  'CASE WHEN C4.Category_ID = "101" AND B4.Soft_Name = "キングスナイト" THEN "102" '
        sql +=  'WHEN C4.Category_ID = "101" AND B4.Soft_Name = "テグザー" THEN "102" '
        sql +=  'WHEN C4.Category_ID = "101" AND B4.Soft_Name = "ファイナルファンタジー" THEN "102" '
        sql +=  'ELSE C4.Category_ID '
        sql +=  'END Category_ID, '
        sql +=  'C4.Category_Group as Category_Group '        
        sql +=  'FROM dqc_item as A4 '
        sql +=  'INNER JOIN dqc_soft as B4 '
        sql +=  'on A4.Soft_Keyname4 = B4.Soft_Keyname '
        sql +=  'LEFT JOIN dqc_category as C4 '
        sql +=  'on A4.Category_key = C4.Category_Key '        

        sql +=  'union '

        sql +=  'SELECT '
        sql +=  'A5.id as id, '
        sql +=  'A5.Sort_no as Sort_no, '
        sql +=  'A5.Preface as Preface,'
        sql +=  'A5.Comment as Comment, '
        sql +=  'A5.Image_ID as Image_ID, '
        sql +=  'A5.Picpath5 as Picpath, '
        sql +=  'A5.Item_Classification as ItemC, '
        sql +=  'A5.Thumbnail5 as Thumb, '
        sql +=  'A5.Alt5 as Alt, '                
        sql +=  'B5.Soft_ID as Soft_ID, '
        sql +=  'B5.Soft_Keyname as Soft_Keyname, '
        sql +=  'B5.Soft_Name_Short as Soft_Name_Short, '
        sql +=  'B5.Soft_Name as Soft_Name, '
        sql +=  'CASE Category_Name WHEN "テレホンカード 1987-1996" THEN "テレホンカード" '
        sql +=  'WHEN "テレホンカード 1997-1998" THEN "テレホンカード" '
        sql +=  'WHEN "テレホンカード 1999-2002" THEN "テレホンカード" '
        sql +=  'WHEN "クロノトリガー プリズムカード" THEN "プリズムカード" '
        sql +=  'WHEN "FFⅤカードコレクションズ" THEN "カードコレクションズ" '       
        sql +=  'WHEN "ファミコンスナック FFⅡ PART1" THEN "ファミコンスナック PART1" '        
        sql +=  'WHEN "ファミコンスナック FFⅡ PART2" THEN "ファミコンスナック PART2" '
        sql +=  'WHEN "FFⅥカードダス PART1" THEN "カードダス PART1" ' 
        sql +=  'WHEN "FFⅥカードダス PART2" THEN "カードダス PART2" '        
        sql +=  'WHEN "PC88・98・FM-7・X1・MSX" THEN "" '
        sql +=  'WHEN "ファミコン・ディスクシステム" THEN "" '        
        sql +=  'WHEN "ゲームボーイ" THEN "" '
        sql +=  'WHEN "スーパーファミコン" THEN "" '        
        sql +=  'WHEN "付録 FC・FCD・GB" THEN "付録" '
        sql +=  'WHEN "付録 SFC" THEN "付録" '
        sql +=  'WHEN "攻略本 FC・FCD・GB" THEN "攻略本" '
        sql +=  'WHEN "攻略本 SFC" THEN "攻略本" '
        sql +=  'WHEN "マリオＲＰＧ トップサンシール" THEN "トップサンシール" '
        sql +=  'ELSE Category_Name '
        sql +=  'END Category_Name, '
        sql +=  'CASE WHEN C5.Category_ID = "101" AND B5.Soft_Name = "キングスナイト" THEN "102" '
        sql +=  'WHEN C5.Category_ID = "101" AND B5.Soft_Name = "テグザー" THEN "102" '
        sql +=  'WHEN C5.Category_ID = "101" AND B5.Soft_Name = "ファイナルファンタジー" THEN "102" '
        sql +=  'ELSE C5.Category_ID '
        sql +=  'END Category_ID, '
        sql +=  'C5.Category_Group as Category_Group '        
        sql +=  'FROM dqc_item as A5 '
        sql +=  'INNER JOIN dqc_soft as B5 '
        sql +=  'on A5.Soft_Keyname5 = B5.Soft_Keyname '
        sql +=  'LEFT JOIN dqc_category as C5 '
        sql +=  'on A5.Category_key = C5.Category_Key '        

        sql +=  'union '

        sql +=  'SELECT '
        sql +=  'A6.id as id, '
        sql +=  'A6.Sort_no as Sort_no, '
        sql +=  'A6.Preface as Preface,'
        sql +=  'A6.Comment as Comment, '
        sql +=  'A6.Image_ID as Image_ID, '
        sql +=  'A6.Picpath6 as Picpath, '
        sql +=  'A6.Item_Classification as ItemC, '
        sql +=  'A6.Thumbnail6 as Thumb, '
        sql +=  'A6.Alt6 as Alt, '         
        sql +=  'B6.Soft_ID as Soft_ID, '
        sql +=  'B6.Soft_Keyname as Soft_Keyname, '
        sql +=  'B6.Soft_Name_Short as Soft_Name_Short, '
        sql +=  'B6.Soft_Name as Soft_Name, '
        sql +=  'CASE Category_Name WHEN "テレホンカード 1987-1996" THEN "テレホンカード" '
        sql +=  'WHEN "テレホンカード 1997-1998" THEN "テレホンカード" '
        sql +=  'WHEN "テレホンカード 1999-2002" THEN "テレホンカード" '
        sql +=  'WHEN "クロノトリガー プリズムカード" THEN "プリズムカード" '
        sql +=  'WHEN "FFⅤカードコレクションズ" THEN "カードコレクションズ" '   
        sql +=  'WHEN "ファミコンスナック FFⅡ PART1" THEN "ファミコンスナック PART1" '        
        sql +=  'WHEN "ファミコンスナック FFⅡ PART2" THEN "ファミコンスナック PART2" '
        sql +=  'WHEN "FFⅥカードダス PART1" THEN "カードダス PART1" ' 
        sql +=  'WHEN "FFⅥカードダス PART2" THEN "カードダス PART2" '        
        sql +=  'WHEN "PC88・98・FM-7・X1・MSX" THEN "" '
        sql +=  'WHEN "ファミコン・ディスクシステム" THEN "" '        
        sql +=  'WHEN "ゲームボーイ" THEN "" '
        sql +=  'WHEN "スーパーファミコン" THEN "" '        
        sql +=  'WHEN "付録 FC・FCD・GB" THEN "付録" '
        sql +=  'WHEN "付録 SFC" THEN "付録" '
        sql +=  'WHEN "攻略本 FC・FCD・GB" THEN "攻略本" '
        sql +=  'WHEN "攻略本 SFC" THEN "攻略本" '
        sql +=  'WHEN "マリオＲＰＧ トップサンシール" THEN "トップサンシール" '
        sql +=  'ELSE Category_Name '
        sql +=  'END Category_Name, '
        sql +=  'CASE WHEN C6.Category_ID = "101" AND B6.Soft_Name = "キングスナイト" THEN "102" '
        sql +=  'WHEN C6.Category_ID = "101" AND B6.Soft_Name = "テグザー" THEN "102" '
        sql +=  'WHEN C6.Category_ID = "101" AND B6.Soft_Name = "ファイナルファンタジー" THEN "102" '
        sql +=  'ELSE C6.Category_ID '
        sql +=  'END Category_ID, '
        sql +=  'C6.Category_Group as Category_Group '        
        sql +=  'FROM dqc_item as A6 '
        sql +=  'INNER JOIN dqc_soft as B6 '
        sql +=  'on A6.Soft_Keyname6 = B6.Soft_Keyname '
        sql +=  'LEFT JOIN dqc_category as C6 '
        sql +=  'on A6.Category_key = C6.Category_Key '        

        sql +=  'union '

        sql +=  'SELECT '
        sql +=  'A7.id as id, '
        sql +=  'A7.Sort_no as Sort_no, '
        sql +=  'A7.Preface as Preface,'
        sql +=  'A7.Comment as Comment, '
        sql +=  'A7.Image_ID as Image_ID, '
        sql +=  'A7.Picpath7 as Picpath, '
        sql +=  'A7.Item_Classification as ItemC, '
        sql +=  'A7.Thumbnail7 as Thumb, '
        sql +=  'A7.Alt7 as Alt, '         
        sql +=  'B7.Soft_ID as Soft_ID, '
        sql +=  'B7.Soft_Keyname as Soft_Keyname, '
        sql +=  'B7.Soft_Name_Short as Soft_Name_Short, '
        sql +=  'B7.Soft_Name as Soft_Name, '
        sql +=  'CASE Category_Name WHEN "テレホンカード 1987-1996" THEN "テレホンカード" '
        sql +=  'WHEN "テレホンカード 1997-1998" THEN "テレホンカード" '
        sql +=  'WHEN "テレホンカード 1999-2002" THEN "テレホンカード" '
        sql +=  'WHEN "クロノトリガー プリズムカード" THEN "プリズムカード" '
        sql +=  'WHEN "FFⅤカードコレクションズ" THEN "カードコレクションズ" '        
        sql +=  'WHEN "ファミコンスナック FFⅡ PART1" THEN "ファミコンスナック PART1" '        
        sql +=  'WHEN "ファミコンスナック FFⅡ PART2" THEN "ファミコンスナック PART2" '
        sql +=  'WHEN "FFⅥカードダス PART1" THEN "カードダス PART1" ' 
        sql +=  'WHEN "FFⅥカードダス PART2" THEN "カードダス PART2" '        
        sql +=  'WHEN "PC88・98・FM-7・X1・MSX" THEN "" '
        sql +=  'WHEN "ファミコン・ディスクシステム" THEN "" '        
        sql +=  'WHEN "ゲームボーイ" THEN "" '
        sql +=  'WHEN "スーパーファミコン" THEN "" '        
        sql +=  'WHEN "付録 FC・FCD・GB" THEN "付録" '
        sql +=  'WHEN "付録 SFC" THEN "付録" '
        sql +=  'WHEN "攻略本 FC・FCD・GB" THEN "攻略本" '
        sql +=  'WHEN "攻略本 SFC" THEN "攻略本" '
        sql +=  'WHEN "マリオＲＰＧ トップサンシール" THEN "トップサンシール" '
        sql +=  'ELSE Category_Name '
        sql +=  'END Category_Name, '
        sql +=  'CASE WHEN C7.Category_ID = "101" AND B7.Soft_Name = "キングスナイト" THEN "102" '
        sql +=  'WHEN C7.Category_ID = "101" AND B7.Soft_Name = "テグザー" THEN "102" '
        sql +=  'WHEN C7.Category_ID = "101" AND B7.Soft_Name = "ファイナルファンタジー" THEN "102" '
        sql +=  'ELSE C7.Category_ID '
        sql +=  'END Category_ID, '
        sql +=  'C7.Category_Group as Category_Group '        
        sql +=  'FROM dqc_item as A7 '
        sql +=  'INNER JOIN dqc_soft as B7 '
        sql +=  'on A7.Soft_Keyname7 = B7.Soft_Keyname '
        sql +=  'LEFT JOIN dqc_category as C7 '
        sql +=  'on A7.Category_key = C7.Category_Key '        

        sql +=  'union '

        sql +=  'SELECT '
        sql +=  'A8.id as id, '
        sql +=  'A8.Sort_no as Sort_no, '
        sql +=  'A8.Preface as Preface,'
        sql +=  'A8.Comment as Comment, '
        sql +=  'A8.Image_ID as Image_ID, '
        sql +=  'A8.Picpath8 as Picpath, '
        sql +=  'A8.Item_Classification as ItemC, '
        sql +=  'A8.Thumbnail8 as Thumb, '
        sql +=  'A8.Alt8 as Alt, '         
        sql +=  'B8.Soft_ID as Soft_ID, '
        sql +=  'B8.Soft_Keyname as Soft_Keyname, '
        sql +=  'B8.Soft_Name_Short as Soft_Name_Short, '
        sql +=  'B8.Soft_Name as Soft_Name, '  
        sql +=  'CASE Category_Name WHEN "テレホンカード 1987-1996" THEN "テレホンカード" '
        sql +=  'WHEN "テレホンカード 1997-1998" THEN "テレホンカード" '
        sql +=  'WHEN "テレホンカード 1999-2002" THEN "テレホンカード" '
        sql +=  'WHEN "クロノトリガー プリズムカード" THEN "プリズムカード" '
        sql +=  'WHEN "FFⅤカードコレクションズ" THEN "カードコレクションズ" '       
        sql +=  'WHEN "ファミコンスナック FFⅡ PART1" THEN "ファミコンスナック PART1" '        
        sql +=  'WHEN "ファミコンスナック FFⅡ PART2" THEN "ファミコンスナック PART2" '
        sql +=  'WHEN "FFⅥカードダス PART1" THEN "カードダス PART1" ' 
        sql +=  'WHEN "FFⅥカードダス PART2" THEN "カードダス PART2" '        
        sql +=  'WHEN "PC88・98・FM-7・X1・MSX" THEN "" '
        sql +=  'WHEN "ファミコン・ディスクシステム" THEN "" '        
        sql +=  'WHEN "ゲームボーイ" THEN "" '
        sql +=  'WHEN "スーパーファミコン" THEN "" '        
        sql +=  'WHEN "付録 FC・FCD・GB" THEN "付録" '
        sql +=  'WHEN "付録 SFC" THEN "付録" '
        sql +=  'WHEN "出版本 FC・FCD・GB" THEN "出版本" '
        sql +=  'WHEN "出版本 SFC" THEN "出版本" '
        sql +=  'WHEN "マリオＲＰＧ トップサンシール" THEN "トップサンシール" '
        sql +=  'ELSE Category_Name '
        sql +=  'END Category_Name, '
        sql +=  'CASE WHEN C8.Category_ID = "101" AND B8.Soft_Name = "キングスナイト" THEN "102" '
        sql +=  'WHEN C8.Category_ID = "101" AND B8.Soft_Name = "テグザー" THEN "102" '
        sql +=  'WHEN C8.Category_ID = "101" AND B8.Soft_Name = "ファイナルファンタジー" THEN "102" '
        sql +=  'ELSE C8.Category_ID '
        sql +=  'END Category_ID, '
        sql +=  'C8.Category_Group as Category_Group '        
        sql +=  'FROM dqc_item as A8 '
        sql +=  'INNER JOIN dqc_soft as B8 '
        sql +=  'on A8.Soft_Keyname8 = B8.Soft_Keyname '
        sql +=  'LEFT JOIN dqc_category as C8 '
        sql +=  'on A8.Category_key = C8.Category_Key '        

        sql +=  ') as D '
        sql +=  'WHERE D.Soft_ID=%(SortID)s '
        sql +=  'ORDER BY D.Category_ID, D.Sort_No '

#        sql2 =  'SELECT * FROM dqc_image as A '
#        sql2 +=  'INNER JOIN dqc_soft as B '
#        sql2 +=  'on A.Soft_Keyname = B.Soft_Keyname '
#        sql2 +=  'LEFT JOIN dqc_category as C '
#        sql2 +=  'on A.Category_key = C.Category_Key '
#        sql2 +=  'WHERE B.Soft_ID=%(SortID)s '

        sql2 =  'select count(datacount) as datacount from ('
        sql2 +=  'SELECT concat(Item_Classification, concat(Soft_KeyName1 , Picpath1)) as datacount, '
        sql2 +=  'B.Soft_ID as Soft_ID FROM dqc_item as A INNER JOIN dqc_soft as B on A.Soft_Keyname1 = B.Soft_Keyname '
        sql2 +=  'union '
        sql2 +=  'SELECT concat(Item_Classification, concat(Soft_KeyName2 , Picpath2)) as datacount, '
        sql2 +=  'B.Soft_ID as Soft_ID FROM dqc_item as A INNER JOIN dqc_soft as B on A.Soft_Keyname2 = B.Soft_Keyname '
        sql2 +=  'union '
        sql2 +=  'SELECT concat(Item_Classification, concat(Soft_KeyName3 , Picpath3)) as datacount, '
        sql2 +=  'B.Soft_ID as Soft_ID FROM dqc_item as A INNER JOIN dqc_soft as B on A.Soft_Keyname3 = B.Soft_Keyname '
        sql2 +=  'union '
        sql2 +=  'SELECT concat(Item_Classification, concat(Soft_KeyName4 , Picpath4)) as datacount, '
        sql2 +=  'B.Soft_ID as Soft_ID FROM dqc_item as A INNER JOIN dqc_soft as B on A.Soft_Keyname4 = B.Soft_Keyname '
        sql2 +=  'union '
        sql2 +=  'SELECT concat(Item_Classification, concat(Soft_KeyName5 , Picpath5)) as datacount, '
        sql2 +=  'B.Soft_ID as Soft_ID FROM dqc_item as A INNER JOIN dqc_soft as B on A.Soft_Keyname5 = B.Soft_Keyname '
        sql2 +=  'union '
        sql2 +=  'SELECT concat(Item_Classification, concat(Soft_KeyName6 , Picpath6)) as datacount, '
        sql2 +=  'B.Soft_ID as Soft_ID FROM dqc_item as A INNER JOIN dqc_soft as B on A.Soft_Keyname6 = B.Soft_Keyname '
        sql2 +=  'union '
        sql2 +=  'SELECT concat(Item_Classification, concat(Soft_KeyName7 , Picpath7)) as datacount, '
        sql2 +=  'B.Soft_ID as Soft_ID FROM dqc_item as A INNER JOIN dqc_soft as B on A.Soft_Keyname7 = B.Soft_Keyname '
        sql2 +=  'union '
        sql2 +=  'SELECT concat(Item_Classification, concat(Soft_KeyName8 , Picpath8)) as datacount, '
        sql2 +=  'B.Soft_ID as Soft_ID FROM dqc_item as A INNER JOIN dqc_soft as B on A.Soft_Keyname8 = B.Soft_Keyname '
        sql2 +=  ') as C '        
        sql2 +=  'WHERE C.Soft_ID=%(SortID)s '
        
        params = {"SortID": pk}
        
        strSoft = Soft.objects.filter(Soft_ID=pk).values('Soft_Name_Short')
        SearchData(Provider=self.request._current_scheme_host, SearchName=strSoft ).save()

        item_count = Item.objects.raw(sql2, params)
        
        context.update({
            'category_list': Category.objects.all().filter(Delete_Flg='0').order_by('id'),
            'item_list': Item.objects.raw(sql, params),
        })
        context['FileName'] = 'Soft'
        context['item_count'] = Item.objects.all().count()  
        return context

    def get_queryset(self):
        return Soft.objects.all().filter(Classification='1').order_by('id')
        
class CategoryView(ListView):
    template_name = 'category.html'
    context_object_name = 'soft_list'
    model = Soft

    def get_context_data(self, **kwargs):
        context = super(CategoryView, self).get_context_data(**kwargs)
        pk = self.kwargs['pk']

        sql =   'SELECT * FROM ( SELECT '
        sql +=  'A1.id as id, '
        sql +=  'A1.Sort_no as Sort_no, '
        sql +=  'A1.Preface as Preface,'
        sql +=  'A1.Comment as Comment, '
        sql +=  'A1.Image_ID as Image_ID, '
        sql +=  'A1.Picpath1 as Picpath, '
        sql +=  'A1.Thumbnail1 as Thumb, '        
        sql +=  'A1.Alt1 as Alt, '
        sql +=  'A1.Item_Classification as ItemC, '        
        sql +=  'B1.Soft_ID as Soft_ID, '
        sql +=  'B1.Soft_Keyname as Soft_Keyname, '
        sql +=  'B1.Soft_Name_Short as Soft_Name_Short, '
        sql +=  'B1.Soft_Name as Soft_Name, ' 
        sql +=  'CASE Category_Name WHEN "テレホンカード 1987-1996" THEN "テレホンカード" '
        sql +=  'WHEN "テレホンカード 1997-1998" THEN "テレホンカード" '
        sql +=  'WHEN "テレホンカード 1999-2002" THEN "テレホンカード" '
        sql +=  'WHEN "クロノトリガー プリズムカード" THEN "プリズムカード" '
        sql +=  'WHEN "FFⅤカードコレクションズ" THEN "カードコレクションズ" '         
        sql +=  'WHEN "ファミコンスナック FFⅡ PART1" THEN "ファミコンスナック PART1" '        
        sql +=  'WHEN "ファミコンスナック FFⅡ PART2" THEN "ファミコンスナック PART2" '
        sql +=  'WHEN "FFⅥカードダス PART1" THEN "カードダス PART1" ' 
        sql +=  'WHEN "FFⅥカードダス PART2" THEN "カードダス PART2" '        
        sql +=  'WHEN "PC88・98・FM-7・X1・MSX" THEN "" '
        sql +=  'WHEN "ファミコン・ディスクシステム" THEN "" '        
        sql +=  'WHEN "ゲームボーイ" THEN "" '
        sql +=  'WHEN "スーパーファミコン" THEN "" '        
        sql +=  'WHEN "付録 FC・FCD・GB" THEN "付録" '
        sql +=  'WHEN "付録 SFC" THEN "付録" '
        sql +=  'WHEN "攻略本 FC・FCD・GB" THEN "攻略本" '
        sql +=  'WHEN "攻略本 SFC" THEN "攻略本" '
        sql +=  'WHEN "マリオＲＰＧ トップサンシール" THEN "トップサンシール" '        
        sql +=  'ELSE Category_Name '
        sql +=  'END Category_Name, '
        sql +=  'C1.Category_ID as Category_ID, '
        sql +=  'C1.Category_Group as Category_Group '
        sql +=  'FROM dqc_item as A1 '
        sql +=  'INNER JOIN dqc_soft as B1 '
        sql +=  'on A1.Soft_Keyname1 = B1.Soft_Keyname '
        sql +=  'LEFT JOIN dqc_category as C1 '
        sql +=  'on A1.Category_key = C1.Category_Key '        

        sql +=  ') as D '
        sql +=  'WHERE D.Category_ID=%(CategoryID)s '
        sql +=  'ORDER BY D.Soft_ID, D.Category_ID, D.Sort_No  '

        sql2 =  'SELECT * FROM dqc_image as A '
        sql2 +=  'INNER JOIN dqc_soft as B '
        sql2 +=  'on A.Soft_Keyname = B.Soft_Keyname '
        sql2 +=  'LEFT JOIN dqc_category as C '
        sql2 +=  'on A.Category_key = C.Category_Key '
        sql2 +=  'where C.Category_ID=%(CategoryID)s '
        sql2 +=  'order by B.Soft_ID'

        params = {"CategoryID": pk}
        
        strCategory = Category.objects.filter(Category_ID=pk).values('Category_Name')
        SearchData(Provider=self.request._current_scheme_host, SearchName=strCategory ).save()

        context.update({
            'category_list': Category.objects.all().filter(Delete_Flg='0').order_by('id'),
            'item_list': Item.objects.raw(sql, params),
            'image_list': Image.objects.raw(sql2, params),
        })

        context['FileName'] = 'Category'
        context['item_count'] = Item.objects.all().count()          
        return context

    def get_queryset(self):
        return Soft.objects.all().filter(Classification='1').order_by('id')

class HistoryView(ListView):
    template_name = "history.html"
    context_object_name = 'history_list'    
    model = History

    def get_context_data(self, **kwargs):
        context = super(HistoryView, self).get_context_data(**kwargs)

        SearchData(Provider=self.request._current_scheme_host, SearchName="History").save()        

        context.update({
            'soft_list': Soft.objects.all().filter(Classification='1').order_by('id'),
            'category_list': Category.objects.all().filter(Delete_Flg='0').order_by('id'),
        })
        context['FileName'] = 'History'
        return context

    def get_queryset(self):
        return History.objects.filter(Delete_Flg='0')

class WantedView(ListView):
    template_name = 'wanted.html'
    context_object_name = 'wanted_list'
    model = Wanted

    def get_context_data(self, **kwargs):
        context = super(WantedView, self).get_context_data(**kwargs)

        SearchData(Provider=self.request._current_scheme_host, SearchName="Wanted").save()
        
        context.update({
            'soft_list': Soft.objects.all().filter(Classification='1').order_by('id'),
            'category_list': Category.objects.all().filter(Delete_Flg='0').order_by('id'),
        })
        context['FileName'] = 'Wanted'
        return context

    def get_queryset(self):
        return Wanted.objects.filter(Delete_Flg='0')
