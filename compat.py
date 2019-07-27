import sys

if sys.version_info[0] < 3:
    def py2_compat(cls):
        if hasattr(cls, 'assertRaisesRegexp'):
            cls.assertRaisesRegex = cls.assertRaisesRegexp
        return cls
else:
    def py2_compat(cls):
        return cls