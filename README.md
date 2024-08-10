# EXIFix
A work-in-progress Python script I wrote for myself to fix errors in metadata caused by moving photos between albums within the Samsung Gallery app. This is especially prevalent with images from WhatsApp, and is hard to fix as they do not contain any EXIF metadata.

================================================================

EXIFix - a tool for fixing messy metadata in your photos

I wrote this tool to fix an issue I've been experiencing when trying to back up photos from my phone (Samsung S9+ with OneUI 2.5/Android 10) to Google Photos or to my computer, where photos appear in the timeline in the wrong place with the wrong date. This is especially noticeable in photos received on WhatsApp.

This tool also doubles as a way to add metadata to photos received on WhatsApp, since they are normally stripped of metadata. The added data is based on the name of the file and uses the date modified that is currently available on the image. This is an imperfect solution, but is the best way I could find to at least make this less of a problem. Depending on when you received and downloaded the image, it may be a couple hours or days away from the actual date the photo was taken.

The root of the problem, and reproducing it:
When you move or copy an image from one album to another within the Samsung Gallery app, it alters the Date Modified. This is why you may have seen old photos show up as recent photos in WhatsApp or Instagram after you move them to another album.

Google Photos, as well as the Photos app on Windows, both follow the Date Modified of image files when placing them in their timelines. This causes a huge mess if you're trying to clean up your gallery. Say you went on a hiking trip last month in August, and now that it's October and you have some free time, you want to move the 200 hiking photos and some photos from your September trips and outings into your main Camera album from the WhatsApp Images album. In the Gallery app, they look fine, since the app uses the Date Taken or Date Created of the images, but once you move them to your computer or upload to Google Photos, you now have these 200+ photos from August and September jammed into the same day and the same minute in October. Your neatly organized albums are thrown out the window.

Fortunately, the date in the filename is preserved, and is the basis of the solution this program aims to use. In some other cases, the date taken is preserved in the EXIF metadata (if not deleted by WhatsApp) of the image. In these cases, if the Date Modified does not match the Date Taken in the metadata, it will be updated.
