import requests
import re
import os
import sys
import pandas as pd
MAX_ID = 807
IMG_SAVE_DIR = "img/"


class Request():
    @classmethod
    def req(cls, url, header_type=""):
        r = requests.get(url, allow_redirects=False)
        if r.status_code != 200:
            print("error")
            print("url:", url)
            print("status code: ", r.status_code)
            return None

        if header_type != "":
            content_type = r.headers["content-type"]
            if header_type not in content_type:
                return None
        return r


class CrawlerImg():
    not_found_message = '<div class="breadcrumb"><a href="/">ホーム</a><span>&gt;</span><strong>ページが見つかりませんでした</strong>'
    pattern = '<div class="profile-phto"><img src="(.+)" alt="(.+)"></div>'

    @classmethod
    def add_to_base_url(cls, uri):
        return "https://www.pokemon.jp" + uri

    @classmethod
    def get_body_or_none(cls, pokemon_id):
        url = CrawlerImg.add_to_base_url(
            "/zukan/detail/{}.html".format(pokemon_id))
        r = Request.req(url)
        if r is None:
            body = None
        else:
            body = r.text.split("\n")
        return body

    @classmethod
    def get_img_info(cls, body):
        body = list(set(body))
        for line in body:
            if ('profile-phto' in line) and ('/zukan/images' in line):
                img_url, pokemon_name = re.findall(CrawlerImg.pattern, line)[0]
                print(img_url, pokemon_name)
        return img_url, pokemon_name


class ImgOpt():
    @classmethod
    def download_image(cls, url):
        r = Request.req(url, "image")
        if r is None:
            return None
        else:
            return r.content

    @classmethod
    def save_image(cls, filename, image):
        try:
            with open(filename, "wb") as f:
                f.write(image)
            return True
        except IOError:
            print("could not save " + filename)
            return False


def save_csv(csv_arr):
    df = pd.DataFrame(csv_arr, columns=['id', 'name', 'image name'])
    # df.to_csv('./output.csv', index=False, header=False)
    df.to_csv('./output.csv', index=False)


def start(start_id, end_id):
    pokemon_id_list = range(start_id, end_id + 1)

    csv_arr = []

    for pokemon_id in pokemon_id_list:
        pokemon_id_zfill = str(pokemon_id).zfill(3)
        body = CrawlerImg.get_body_or_none(pokemon_id_zfill)
        if body is None:
            print("error: ", pokemon_id_zfill)
            continue
        img_uri, pokemon_name = CrawlerImg.get_img_info(body)
        img_url = CrawlerImg.add_to_base_url(img_uri)
        img = ImgOpt.download_image(img_url)
        if img is None:
            print("imgage download error", img_url)
            continue
        image_name = img_uri.split("/")[-1]
        save_file_path = os.path.join(IMG_SAVE_DIR, image_name)
        save_result = ImgOpt.save_image(save_file_path, img)
        if save_result:
            csv_arr.append([pokemon_id_zfill, pokemon_name, image_name])

    save_csv(csv_arr)


def main():
    if len(sys.argv) == 1:
        start_id = 1
        end_id = MAX_ID
    elif len(sys.argv) == 3:
        start_id = int(sys.argv[-2])
        end_id = int(sys.argv[-1])
    else:
        print("invalid number of arguments")
        exit(0)

    start(start_id, end_id)


if __name__ == "__main__":
    main()
