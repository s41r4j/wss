
<p align=center>
  <img src="https://github.com/s41r4j/wss/assets/65067289/e1a5c83b-32f4-4f61-850e-058870cc850b">
</p>

<br>

<b>WebScrapeSite</b> (abbreviated __wss__) is a powerful and user-friendly web scraping tool written in python3. It provides a convenient and efficient way to extract data and insights from websites quickly. Whether you're a _data analyst_, _researcher_, _developer_ or _hacker_, wss can help you gather the information you need from websites with one command. It can efficiently categorize and recover various web components such as hyperlinks, image links, JavaScript resources, stylesheet references, email addresses, whois records and much more, all with remarkable speed and accuracy.

It is equipped with flexible data export options, making it easy to save collected data in either CSV or JSON format. By default, it stores data in a CSV file, a widely accepted and human-readable format. Alternatively, you can choose to export data in JSON, a more structured format preferred by developers and applications. This adaptability ensures that you can seamlessly integrate the collected data into your analysis, research, development or attack workflows while catering to your specific requirements.

> works on linux, windows & android (termux)


<br>

## 💿 Installation:
```
git clone https://github.com/s41r4j/wss/; cd wss; pip install -r requirements.txt
```
> prerequisite: python3, pip, git, internet connection

<br>

## 🧾 Usage:
| _help menu_ | _demo target_ |
|---|---|
| <p align=center> <img src="https://github.com/s41r4j/wss/assets/65067289/fa15e8fd-967e-4638-95ab-f55ef143660a"> </p> | <p align=center> <img src="https://github.com/s41r4j/wss/assets/65067289/623c53b3-5d29-4436-8867-b16e00b6a70d"> </p> |
| `python3 wss.py -h` | `python3 wss.py -u google.com` |
> collocted data is automatically stored in a file (filename in yellow)

<br>
  
- 🗒️ examples:
```
python3 wss.py -u example.com
python3 wss.py -u example.com/example -f json
python3 wss.py -u https://example.com/ -a
```



