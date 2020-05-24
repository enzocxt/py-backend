import json
import time
from utils import log


def save(data, path):
    """
    本函数把一个 dict 或者 list 写入文件
    data 是 dict 或者 list
    path 是保存文件的路径
    """
    # indent 是缩进
    # ensure_ascii=False 用于保存中文
    s = json.dumps(data, indent=2, ensure_ascii=False)
    with open(path, 'w+', encoding='utf-8') as fout:
        log('save:', path, s, data)
        fout.write(s)


def load(path):
    """
    本函数从一个文件中载入数据并转化为 dict 或者 list
    path 是保存文件的路径
    """
    with open(path, 'r', encoding='utf-8') as fin:
        s = fin.read()
        log('load:', s)
        return json.loads(s)


# Model 是用于存储数据的基类
class Model(object):
    @classmethod
    def db_path(cls):
        classname = cls.__name__
        path = 'data/{}.txt'.format(classname)
        return path

    @classmethod
    def new(cls, form):
        # 下面一句相当于 User(form) 或者 Msg(form)
        m = cls(form)
        return m

    @classmethod
    def all(cls):
        """
        得到一个类的所有存储的实例
        """
        path = cls.db_path()
        models = load(path)
        ms = [cls(m) for m in models]
        return ms

    @classmethod
    def find_by(cls, **kwargs):
        """
        用法如下，kwargs 是只有一个元素的 dict
        u = User.find_by(username='gua')
        """
        log('kwargs, ', kwargs)
        k, v = '', ''
        for key, value in kwargs.items():
            k, v = key, value
        all = cls.all()
        for m in all:
            if v == m.__dict__[k]:
                return m
        return None

    @classmethod
    def find_all(cls, **kwargs):
        k, v = '', ''
        for key, value in kwargs.items():
            k, v = key, value
        all = cls.all()
        data = []
        for m in all:
            # getattr(m, k) 等价于 m.__dict__[k]
            if v == m.__dict__[k]:
                data.append(m)
        return data

    def save(self):
        """
        save 方法用于把一个 Model 的实例保存到文件中
        """
        models = self.all()
        log('models:', models)
        if self.__dict__.get('id') is None or self.__dict__.get('id') == -1:
            # 加上 id
            if len(models) > 0:
                # 不是第一个数据
                self.id = models[-1].id + 1
            else:
                # 是第一个数据
                self.id = 1
            models.append(self)
        else:
            # 有 id 说明已经存在于数据文件中
            index = -1
            for i, m in enumerate(models):
                if m.id == self.id:
                    index = i
                    break
            if index > -1:
                # 找到下标，替换数据
                models[index] = self
        # __dict__ 是包含了对象所有属性和值的字典
        m_data = [m.__dict__ for m in models]
        path = self.db_path()
        save(m_data, path)

    def remove(self):
        models = self.all()
        log('models:', models)
        if self.__dict__.get('id') is not None or self.__dict__.get('id') != -1:
            index = -1
            for i, m in enumerate(models):
                if m.id == self.id:
                    index = i
                    break
            if index > -1:
                del models[index]
        m_data = [m.__dict__ for m in models]
        path = self.db_path()
        save(m_data, path)

    def time(self):
        format_ = '%Y/%m/%d %H:%M:%S'
        value = time.localtime(self.ct)
        dt = time.strftime(format_, value)
        return dt

    def __repr__(self):
        """
        当你调用 str(o) 的时候
        实际上调用了 o.__str__()
        当没有 __str__ 的时候
        就调用 __repr__
        """
        classname = self.__class__.__name__
        properties = ['{}: ({})'.format(k, v) for k, v in self.__dict__.items()]
        s = '\n'.join(properties)
        return '< {}\n{} >\n'.format(classname, s)
