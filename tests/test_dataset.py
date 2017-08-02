from __future__ import division, print_function

import unittest

from rvseg import dataset

class TestDataset(unittest.TestCase):
    def test_generator(self):
        self._test_generator(mask='inner')
        self._test_generator(mask='outer')
        self._test_generator(mask='both')

    def test_no_validation(self):
        self._test_no_validation(mask='inner')
        self._test_no_validation(mask='outer')
        self._test_no_validation(mask='both')

    def _test_generator(self, mask):
        data_dir = "../test-assets/"
        batch_size = 2
        validation_split = 0.5
        # With a total of 3 training images, this split will create 1
        # training image and 2 validation images

        (train_generator, train_steps_per_epoch,
         val_generator, val_steps_per_epoch) = dataset.create_generators(
             data_dir, batch_size,
             validation_split=validation_split,
             mask=mask)

        self.assertEqual(train_steps_per_epoch, 1)
        self.assertEqual(val_steps_per_epoch, 1)

        classes = 3 if mask == 'both' else 2

        images, masks = next(train_generator)
        self.assertEqual(images.shape, (1, 216, 256, 1))
        self.assertEqual(masks.shape, (1, 216, 256, classes))

        images, masks = next(val_generator)
        self.assertEqual(images.shape, (2, 216, 256, 1))
        self.assertEqual(masks.shape, (2, 216, 256, classes))

    def _test_no_validation(self, mask):
        data_dir = "../test-assets/"
        batch_size = 2
        validation_split = 0.0

        (train_generator, train_steps_per_epoch,
         val_generator, val_steps_per_epoch) = dataset.create_generators(
             data_dir, batch_size,
             validation_split=validation_split,
             mask=mask)

        self.assertEqual(train_steps_per_epoch, 2)
        self.assertEqual(val_steps_per_epoch, 0)

        classes = 3 if mask == 'both' else 2

        # first 2 train images
        images, masks = next(train_generator)
        self.assertEqual(images.shape, (2, 216, 256, 1))
        self.assertEqual(masks.shape, (2, 216, 256, classes))

        # last train image (for total of 3)
        images, masks = next(train_generator)
        self.assertEqual(images.shape, (1, 216, 256, 1))
        self.assertEqual(masks.shape, (1, 216, 256, classes))

        # first 2 train images again
        images, masks = next(train_generator)
        self.assertEqual(images.shape, (2, 216, 256, 1))
        self.assertEqual(masks.shape, (2, 216, 256, classes))

        # validation generator should be nothing
        self.assertEqual(val_generator, None)
