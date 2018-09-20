# QiitaPy

---

QiitaPy is the Vim plugin to edit articles on Qiita.
It's written in Python.

## Requirement

- environment
    - python3
- python library
    - vim
    - [petitviolet/qiita\_py](https://github.com/petitviolet/qiita_py)

## Install

Write the following in .vimrc.

- dein.vim:
```
call dein#add('Kenta11/qiita-py')
```

- neubundle:
```
NeoBundle 'Kenta11/qiita-py'
```

## Easy tutorial

Let's post an article to Qiita with QiitaPy!

### Setting a config file

First, create *access token* on [Qiita](https://qiita.com/settings/applications).
After making a memo, use config command and write access token.
I'd recommended to write your username in *USER_NAME*.
Then, close the Vim.
```
:QiitaPy config
```
![image-config](img/config.png)


### Write an article

Next, generate a template file with the following command.
Upper block of the template is yaml meta data.
You can write title and tags in it.
```
:QiitaPy template
```
![image-template](img/template.png)

### Post to Qiita!

If you finish to write an article, let's post to Qiita.
If you are posting the article for the first time, add *new* option.
```
:QiitaPy post new
```
![image-template](img/post.png)

Check your page on Qiita!
![image-template](img/Qiita.png)

## Licence

[MIT License](LICENSE)

## Link

Comming soon...

## Author

Kenta Arai
- [Twitter](https://twitter.com/isKenta14)

