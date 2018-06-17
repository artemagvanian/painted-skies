import cv2

from syndicate.color_distinguisher import ColorDistinguisher
from syndicate.multi_color_processor import MultiColorProcessor
from syndicate.ocr_applier import OCRApplier
from syndicate.string_builder import StringBuilder
from syndicate.tree_builder import TreeBuilder


class Syndicate():
    '''
    Главный элемент для контроля взаимодействия других частей приложения
    '''

    def process(self, img_path):
        img = cv2.imread(img_path)
        sb = StringBuilder()
        strings = sb.to_strings(img)
        mcp = MultiColorProcessor()
        crops = mcp.get_crops_from_strings(strings)
        cd = ColorDistinguisher()
        levels = cd.distinguish(crops)
        ocra = OCRApplier()
        crop_infos = ocra.recognize(levels)
        tb = TreeBuilder()
        tb.build(crop_infos)
