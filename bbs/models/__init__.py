import time
import json
from utils import log


def save(data, path):
    """
    data 是 dict 或者 list
    path 是保存文件的路径
    """
    s = json.dumps(data, indent=2, ensure_ascii=False)
    with open(path, 'w+', encoding='utf-8') as f:
        # log('save', path, s, data)
        f.write(s)


def load(path):
    with open(path, 'r', encoding='utf-8') as f:
        s = f.read()
        # log('load', s)
        return json.loads(s)


# Model 是一个 ORM（object relation mapper）
# 好处就是不需要关心存储数据的细节，直接使用即可
class Model(object):
    """
    Model 是所有 model 的基类
    """
    @classmethod
    def db_path(cls):
        """
        数据存放路径，暂时使用 txt 文件模拟数据库
        """
        classname = cls.__name__
        path = f'data/{classname}.txt'
        return path

    @classmethod
    def _new_from_dict(cls, d):
        # 因为子元素的 __init__ 需要一个 form 参数
        # 所以这个给一个空字典
        m = cls({})
        for k, v in d.items():
            # setattr 是一个特殊的函数
            # 假设 k v 分别是 'name'  'gua'
            # 它相当于 m.name = 'gua'
            setattr(m, k, v)
        return m

    @classmethod
    def new(cls, form, **kwargs):
        m = cls(form)
        # 额外地设置 m 的属性
        for k, v in kwargs.items():
            # 设置对象的属性
            setattr(m, k, v)
        m.save()
        return m

    @classmethod
    def all(cls):
        """
        all 方法使用 load 函数得到所有的 models
        """
        path = cls.db_path()
        models = load(path)
        ms = [cls._new_from_dict(m) for m in models]
        return ms

    @classmethod
    def find_all(cls, **kwargs):
        ms = []
        k, v = '', ''
        # 其实就是取出一个键值对
        for key, val in kwargs.items():
            k, v = key, val
        all = cls.all()
        for m in all:
            # 也可以用 getattr(m, k) 取值
            if v == m.__dict__[k]:
                ms.append(m)
        return ms

    @classmethod
    def find_by(cls, **kwargs):
        """
        kwargs 是只有一个元素的 dict
        用法：u = User.find_by(username='gua')
        """
        k, v = '', ''
        for key, val in kwargs.items():
            k, v = key, val
        all = cls.all()
        for m in all:
            if v == m.__dict__[k]:
                return m
        return None

    @classmethod
    def find(cls, id):
        return cls.find_by(id=id)

    @classmethod
    def get(cls, id):
        return cls.find_by(id=id)

    @classmethod
    def delete(cls, id):
        models = cls.all()
        index = -1
        for i, e in enumerate(models):
            if e.id == id:
                index = i
                break
            if index == -1:
                pass
            else:
                obj = models.pop(index)
                rest = [m.__dict__ for m in models]
                path = cls.db_path()
                save(rest, path)
                return obj

    def __repr__(self):
        classname = self.__class__.__name__
        properties = ['{}: ({})'.format(k, v) for k, v in self.__dict__.items()]
        s = '\n'.join(properties)
        return '< {}\n{} \n>\n'.format(classname, s)

    def to_json(self):
        """
        返回当前 model 的字典表示
        """
        d = self.__dict__.copy()
        return d

    def save(self):
        """
        用 all 方法读取文件中的所有 model 并生成一个 list
        把 self 添加进去并且保存进文件
        """
        models = self.all()
        # 如果没有 id，说明是新添加的元素
        if self.id is None:
            if len(models) == 0:
                self.id = 1
            else:
                m = models[-1]
                self.id = m.id + 1
            models.append(self)
        else:
            index = -1
            for i, m in enumerate(models):
                if m.id == self.id:
                    index = i
                    break
            models[index] = self
        new_models = [m.__dict__ for m in models]
        path = self.db_path()
        save(new_models, path)
