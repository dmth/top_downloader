# top_downloader
Bulk-downloads DTK25, DTK50 or DTK100 maps in PDF-format from https://www.opengeodata.nrw.de/produkte/geobasis/tk/

This software is in a "works for me" state.
This means it is not fit for production.

Opengeodata.nrw also offers DTK10 maps as zipped tiff files, see:
https://www.opengeodata.nrw.de/produkte/geobasis/tk/dtk10nrw/dtk10nrw_farbe_tiff_paketiert/

and also DGK5 as zipped tiff:
https://www.opengeodata.nrw.de/produkte/geobasis/tk/dgk5/dgk5_gru_tiff_paketiert/

## License
 - This software is provided under the MIT - License.
 - The data-products downloaded by this software are provided under the "Data licence Germany - Zero - Version 2.0". See: https://www.govdata.de/dl-de/zero-2-0


## Usage

```
python3 top_downloader.py --help
```

You can choose between dtk25, dtk50 and dtk100 maps, by selecting the product with the ```--product``` parameter.

All maps are downloaded to your ```\tmp```folder or similar folders on non-linux machines.
