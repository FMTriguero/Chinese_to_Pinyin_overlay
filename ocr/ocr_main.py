from ocr.detector.detector import Detector
from ocr.recognizer.recognizer import Recognizer
from ocr import util

import asyncio
import numpy as np


def _awaitable(f, *args):
    return asyncio.get_running_loop().run_in_executor(None, f, *args)


class Ocr:
    def __init__(self):
        self.detector = Detector()
        self.recognizer = Recognizer()

    async def get_results(self, image):
        image_to_screen = [1, 1]

        result, _ = await _awaitable(self.get_characters_from_screen, image)

        sentences = [{"text": r[1], "position": r[0][:2]} for r in result.values()]

        results = []
        for sentence in sentences:
            orig_text = sentence["text"]
            if util.contains_chinese(orig_text):
                pinyin_text = util.get_pinyin(orig_text)
                translations = util.get_all_phrase_translations(orig_text)
                translation_text = "\n".join(
                    ["%s (%s): %s" % (t[0], util.get_pinyin(t[0]), ", ".join(t[1])) for t in translations])

                position = (
                    int(sentence["position"][0] * image_to_screen[0]),
                    int((sentence["position"][1] * image_to_screen[1]) + 20)
                )

                results.append({
                    "text": orig_text,
                    "position": position,
                    "pinyin_text": pinyin_text,
                    "translation_text": translation_text
                })

        return results

    def get_characters_from_screen(self, image):
        text_recs, img_framed, image = self.detector.detect(image)
        text_recs = util.sort_box(text_recs)
        
        result = self.recognize_characters(image, text_recs)

        return result, img_framed

    def recognize_characters(self, image, text_recs):
        results = {}
        x_dim, y_dim = image.shape[1], image.shape[0]

        for index, rec in enumerate(text_recs):

            pt1 = (max(1, rec[0]), max(1, rec[1]))
            pt2 = (rec[2], rec[3])
            pt3 = (min(rec[6], x_dim - 2), min(y_dim - 2, rec[7]))
            pt4 = (rec[4], rec[5])

            degree = np.degrees(np.arctan2(
                pt2[1] - pt1[1], pt2[0] - pt1[0]))

            part_image = util.dump_rotate_image(image, degree, pt1, pt2, pt3, pt4)

            if part_image.shape[0] < 1 or part_image.shape[1] < 1 or part_image.shape[0] > part_image.shape[1]:
                continue
            text = self.recognizer.recognize(part_image)
            if len(text) > 0:
                results[index] = [rec]
                results[index].append(text)

        return results
