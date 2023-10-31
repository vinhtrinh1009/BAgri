import 'package:cached_network_image/cached_network_image.dart';
import 'package:flutter/material.dart';
import 'package:flutter_base/commons/app_images.dart';
import 'package:photo_view/photo_view.dart';
import 'package:smooth_page_indicator/smooth_page_indicator.dart';

class PhotosDialog extends StatelessWidget {
  PageController? _controller;
  final List<String?> images;
  final int selectedIndex;
  final bool closeButton;

  PhotosDialog(
      {required this.images,
      this.selectedIndex = 0,
      this.closeButton = false}) {
    _controller = PageController(initialPage: selectedIndex);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.transparent,
      body: Stack(
        //alignment: Alignment.center,
        children: [
          _buildListImage(),
          Positioned(
              right: closeButton ? 0 : null,
              left: closeButton ? null : 0,
              top: closeButton ? 0 : 12,
              child: _buildBackButton(context)),
          Positioned(
              left: 0,
              bottom: 60,
              right: 0,
              child:
                  Visibility(visible: images.length > 1, child: _smoothPage())),
        ],
      ),
    );
  }

  Widget _buildListImage() {
    List<Widget> list = [];
    images.forEach((element) {
      list.add(_imageWidget(image: element ?? ""));
    });
    return PageView(
      controller: _controller,
      children: list,
    );
  }

  Widget _imageWidget({required String image}) {
    return PhotoView(
      backgroundDecoration: BoxDecoration(
        color: Colors.transparent,
      ),
      imageProvider: CachedNetworkImageProvider(image),
      minScale: PhotoViewComputedScale.contained,
      maxScale: PhotoViewComputedScale.contained * 5,
    );
  }

  Widget _smoothPage() {
    return Container(
      alignment: Alignment.center,
      child: SmoothPageIndicator(
        controller: _controller!,
        count: images.length,
        effect: ExpandingDotsEffect(
          dotWidth: 6,
          dotHeight: 6,
          expansionFactor: 2,
          spacing: 3,
          dotColor: Colors.white,
          activeDotColor: Color(0xFFFFA700).withOpacity(0.5),
        ),
      ),
    );
  }

  Widget _buildBackButton(BuildContext context) {
    return GestureDetector(
      onTap: () {
        Navigator.of(context).pop();
      },
      child: Container(
        width: 40,
        height: 48,
        color: Colors.transparent,
        child: Center(
          child: !closeButton
              ? Image.asset(AppImages.icBack)
              : Icon(
                  Icons.close,
                  color: Colors.white,
                ),
        ),
      ),
    );
  }
}
