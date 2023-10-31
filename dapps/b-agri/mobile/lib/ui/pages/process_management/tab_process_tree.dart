import 'package:flutter/material.dart';
import 'package:flutter_base/ui/pages/process_management/process_listing/process_listing_page.dart';
import 'package:flutter_base/ui/pages/tree_management/tree_listing/tree_listing_page.dart';
import 'package:flutter_base/ui/widgets/b_agri/app_bar_widget.dart';

class ProcessTabPage extends StatefulWidget {
  @override
  _ProcessTabPageState createState() => _ProcessTabPageState();
}

class _ProcessTabPageState extends State<ProcessTabPage>
    with SingleTickerProviderStateMixin {
  late TabController _controller;

  @override
  void initState() {
    super.initState();
    _controller = TabController(length: 2, vsync: this);
    _controller.addListener(() {
      setState(() {});
    });
  }

  @override
  void dispose() {
    super.dispose();
    _controller.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBarWidget(
        title: "Quản lý quy trình",
        context: context,
      ),
      body: Container(
          child: Padding(
        padding: const EdgeInsets.only(
          top: 9,
        ),
        child: Column(
          children: [
            Container(
              padding: EdgeInsets.symmetric(horizontal: 10),
              child: Row(
                children: [
                  Expanded(
                    child: TabItem(
                      controller: _controller,
                      title: 'Danh sách quy trình',
                      index: 0,
                    ),
                  ),
                  const SizedBox(width: 8),
                  Expanded(
                    child: TabItem(
                      controller: _controller,
                      title: 'Danh sách cây trồng',
                      index: 1,
                    ),
                  ),
                ],
              ),
            ),
            const SizedBox(height: 9),
            Expanded(
              child: TabBarView(
                controller: _controller,
                children: [
                  TabListProcess(),
                  TabListTree(),
                ],
              ),
            ),
          ],
        ),
      )),
    );
  }
}

class TabItem extends StatelessWidget {
  final TabController controller;
  final String title;
  final int index;

  TabItem({required this.controller, required this.title, required this.index});

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: () {
        controller.animateTo(index);
      },
      child: Container(
        padding: const EdgeInsets.symmetric(vertical: 10),
        decoration: BoxDecoration(
          borderRadius: BorderRadius.circular(25),
          color:
              controller.index == index ? Color(0xFF4EC04B) : Color(0xFFECECEC),
        ),
        child: Align(
          alignment: Alignment.center,
          child: Text(
            title,
            style: controller.index == index
                ? const TextStyle(
                    fontSize: 14,
                    fontWeight: FontWeight.bold,
                    color: Color(0xFFFFFFFF))
                : const TextStyle(
                    fontSize: 14,
                    fontWeight: FontWeight.bold,
                    color: Color(0xFF7A7A7A)),
          ),
        ),
      ),
    );
  }
}
