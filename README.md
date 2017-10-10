# top_downloader
Bulk-downloads DTK50 or DTK100 maps in PDF-format from https://www.opengeodata.nrw.de/produkte/geobasis/dtk

This software is in a "works for me" state.
This means it is not fit for production.

## Usage

```
python3 top_downloader.py --help
```

You can choose between dtk50 and dtk100 maps, by selecting the product with the ```--product``` parameter.

All maps are downloaded to your ```\tmp```folder or similar folders on non-linux machines.