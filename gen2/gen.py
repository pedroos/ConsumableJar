#!/usr/bin/env python3
import os.path
from conf import conf
import codecs

full_page_path = os.path.join(conf['gen_dir'], 'fullpage.html')
if not os.path.isfile(full_page_path):
    print(full_page_path + ' not found.')
    exit(1)
with codecs.open(full_page_path, "r", "utf-8") as full_page_file:
    full_page_content = full_page_file.read()

style_header_path = os.path.join(conf['gen_dir'], 'page_style_header.html')
style_body_article_path = os.path.join(conf['gen_dir'], 'page_style_body_article.html')
style_body_article_trad_path = os.path.join(conf['gen_dir'], 'page_style_body_article_trad.html')
if not os.path.isfile(style_header_path):
    print(style_header_path + ' not found.')
    exit(1)
if not os.path.isfile(style_body_article_path):
    print(style_body_article_path + ' not found.')
    exit(1)
if not os.path.isfile(style_body_article_trad_path):
    print(style_body_article_trad_path + ' not found.')
    exit(1)
with codecs.open(style_header_path, "r", "utf-8") as style_file:
    style_header = style_file.read()
    full_page_content = full_page_content.replace('%%style_header%%', style_header)
with codecs.open(style_body_article_path, "r", "utf-8") as style_file:
    style_body_article = style_file.read()
with codecs.open(style_body_article_trad_path, "r", "utf-8") as style_file:
    style_body_article_trad = style_file.read()

header_path = os.path.join(conf['gen_dir'], 'header_'+conf['header']+'.html')
if not os.path.isfile(header_path):
    print(header_path + ' not found.')
    exit(1)
with codecs.open(header_path, "r", "utf-8") as header_file:
    header_content = header_file.read()

# toc_path = os.path.join(conf['gen_dir'], 'page_toc.html')
# if not os.path.isfile(toc_path):
#     print(toc_path + ' not found.')
#     exit(1)
# with codecs.open(toc_path, "r", "utf-8") as toc_file:
#     toc_content = toc_file.read()
# header_content = header_content.replace('%%toc%%', toc_content)

index_page_path = os.path.join(conf['gen_dir'], 'cpage_'+conf['index_page']+'.html')
if not os.path.isfile(index_page_path):
    index_page_path = os.path.join(conf['gen_dir'], 'cnb_'+conf['index_page']+'.html')
    if not os.path.isfile(index_page_path):
        print(index_page_path + ' not found.')
        exit(1)
full_page_content = full_page_content.replace('%%header%%', header_content)

breadcrumb_path = os.path.join(conf['gen_dir'], 'breadcrumb.html')
if not os.path.isfile(breadcrumb_path):
    print(breadcrumb_path + ' not found.')
    exit(1)
with codecs.open(breadcrumb_path, "r", "utf-8") as breadcrumb_file:
    breadcrumb_content = breadcrumb_file.read()

sitepages = ['cpage_toc', 'cpage_about']

# create out dir, if not exists
outdir = os.path.join(conf['gen_dir'], 'out')
if not os.path.exists(outdir):
    os.makedirs(outdir)

# toc page (was a standalone toc page)
# toc_page_path = os.path.join(conf['gen_dir'], 'tocpage.html')
# if not os.path.isfile(toc_page_path):
#    print(toc_page_path + ' not found.')
#    exit(1)
# with codecs.open(toc_page_path, "r", "utf-8") as toc_page_file:
#    toc_page_content = toc_page_file.read()
# toc_page_content = toc_page_content.replace('%%style%%', style_content)
# toc_page_content = toc_page_content.replace('%%content%%', toc_content)
# toc_2_path = os.path.join(conf['gen_dir'], 'toc.html')
# with codecs.open(toc_2_path, "w", "utf-8") as toc_2_file:
#    toc_2_file.write(toc_page_content)
# print(os.path.basename(toc_2_path) + ': wrote.')

# pages
for file in os.listdir(conf['gen_dir']):
    file_path = os.path.join(conf['gen_dir'], file)
    if not os.path.isfile(file_path):
        continue
    filename, extension = os.path.splitext(file)
    if filename.find('_') == -1:
        continue
    if extension != ".html":
        continue
    if not \
        (filename.startswith('cpage_') or \
        filename.startswith('ctrad_')):
        #print('   Skipping %s' % filename)
        continue

    full_content = full_page_content

    if filename.startswith('cpage_'):
        if filename in sitepages:
            body_class = 'sitepage'
        else:
            body_class = 'article'
    elif filename.startswith('ctrad_'):
        body_class = 'trad'
    else:
        body_class = ''
    full_content = full_content.replace('%%body_class%%', body_class)

    full_content = full_content.replace('%%breadcrumb%%', \
        breadcrumb_content if filename not in sitepages else '')
    
    full_content = full_content.replace('%%mathjaxscale%%', \
        '1.15' if body_class == 'trad' else '1')

    # body style is now replaced per-page.
    isNb = filename.startswith('cnb_')
    style_body = style_body_article if not isNb else style_body_nb
    if filename.startswith('ctrad_'):
        style_body = style_body + style_body_article_trad
    full_content = full_content.replace('%%style_body%%', style_body)

    filename_noprefix = filename[filename.index('_')+1:]
    filename_noprefix_ext = filename_noprefix+'.html'
    print(filename_noprefix_ext + ": ", end='')
    filename2 = os.path.join(outdir, filename_noprefix_ext)
    with codecs.open(file_path, "r", "utf-8") as file_file:
        content = file_file.read()
    full_content = full_content.replace('%%content%%', content)

    #delete old same-dir output file, if uncommented
    filename2_old = os.path.join(conf['gen_dir'], filename_noprefix_ext)
    if os.path.exists(filename2_old):
        os.remove(filename2_old)
        print("\n"+filename2_old+" removed.")
    
    #read <h1> and write as <title>
    h1Idx = full_content.find('<h1>')
    title = ''
    if h1Idx == -1:
        print("\n  *warning: article without title (<h1>)")
    else:
        title = full_content[h1Idx+len("<h1>"):]
        h1Idx = title.find('</h1>')
        if h1Idx == -1:
            print("\n  *warning: title without end tag (</h1>), discarding title")
        else:
            title = title[:h1Idx] + " - " + conf['title']
            #print("\n  title: " + title)

    full_content = full_content.replace('%%title%%', title if title != '' else conf['title'])

    with codecs.open(filename2, "w+", "utf-8") as filename2_file:
        filename2_file.write(full_content)
    print('wrote.')

    # /*if (filename.StartsWith("cmart_"))
    # {
    #     filename2 = Path.Combine(genDir, "mart_" + filenameNoPrefix + ".html");
    #     File.WriteAllText(filename2, fullContent);
    #     Console.WriteLine("wrote " + Path.GetFileName(filename2));
    # }*/

    if filename_noprefix == conf['index_page']:
        index_path = os.path.join(outdir, 'index.html')
        print('index.html' + ": ", end='')
        with codecs.open(index_path, "w", "utf-8") as index_file:
            index_file.write(full_content)
            print('wrote.')

print('end.')
exit(0)