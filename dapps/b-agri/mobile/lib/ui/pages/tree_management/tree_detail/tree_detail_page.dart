import 'package:flutter/material.dart';
import 'package:flutter_base/commons/app_colors.dart';
import 'package:flutter_base/commons/app_text_styles.dart';
import 'package:flutter_base/main.dart';
import 'package:flutter_base/models/enums/load_status.dart';
import 'package:flutter_base/router/application.dart';
import 'package:flutter_base/router/routers.dart';
import 'package:flutter_base/ui/pages/tree_management/tree_detail/tree_detail_cubit.dart';
import 'package:flutter_base/ui/pages/tree_management/update_tree/update_tree_page.dart';
import 'package:flutter_base/ui/widgets/b_agri/app_bar_widget.dart';
import 'package:flutter_base/ui/widgets/b_agri/app_button.dart';
import 'package:flutter_base/ui/widgets/b_agri/app_text_field.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

class TreeDetailPage extends StatefulWidget {
  final String? tree_id;
  final String? description;
  final String? name;

  TreeDetailPage({Key? key, this.tree_id, this.name, this.description})
      : super(key: key);

  @override
  _TreeDetailPageState createState() => _TreeDetailPageState();
}

class _TreeDetailPageState extends State<TreeDetailPage> {
  final _formKey = GlobalKey<FormState>();
  late TextEditingController nameController;
  late TextEditingController descriptionController;
  TreeDetailCubit? _cubit;

  @override
  void initState() {
    // TODO: implement initState
    super.initState();
    _cubit = BlocProvider.of<TreeDetailCubit>(context);
    _cubit!.getTreeDetail(widget.tree_id!);
    nameController = TextEditingController(text: '');
    descriptionController = TextEditingController(text: '');
  }

  @override
  void dispose() {
    // TODO: implement dispose
    super.dispose();
    _cubit!.close();
    nameController.dispose();
    descriptionController.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      resizeToAvoidBottomInset: true,
      appBar: AppBarWidget(
        context: context,
        title: 'Chi tiết cây trồng',
      ),
      body: SafeArea(
        child: SingleChildScrollView(
          child: Padding(
            padding: EdgeInsets.symmetric(horizontal: 20, vertical: 15),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                BlocConsumer<TreeDetailCubit, TreeDetailState>(
                  listener: (context, state) {
                    // TODO: implement listener
                    if (state.loadStatus == LoadStatus.SUCCESS) {
                      nameController =
                          TextEditingController(text: state.treeData!.name);
                      descriptionController = TextEditingController(
                          text: state.treeData!.description);
                    }
                  },
                  builder: (context, state) {
                    return Form(
                      key: _formKey,
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(
                            'Tên cây trồng',
                            style: AppTextStyle.greyS14,
                          ),
                          SizedBox(height: 10),
                          AppTextField(
                            hintText: '',
                            controller: nameController,
                            enable: false,
                          ),
                          SizedBox(height: 20),
                          Text(
                            'Mô tả',
                            style: AppTextStyle.greyS14,
                          ),
                          SizedBox(height: 10),
                          AppTextAreaField(
                            hintText: '',
                            maxLines: 8,
                            enable: false,
                            controller: descriptionController,
                          ),
                        ],
                      ),
                    );
                  },
                ),
                SizedBox(
                  height: 50,
                ),
                buildActionCreate(),
              ],
            ),
          ),
        ),
      ),
    );
  }

  Widget buildActionCreate() {
    return Column(
      children: [
        Row(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Expanded(
              child: AppButton(
                color: AppColors.redButton,
                title: 'Hủy bỏ',
                onPressed: () {
                  Navigator.of(context).pop();
                },
              ),
            ),
            SizedBox(width: 40),
            Expanded(
              child: AppButton(
                width: 100,
                color: AppColors.main,
                title: 'Sửa',
                onPressed: () async {
                  bool isUpdate = await Application.router!.navigateTo(
                    appNavigatorKey.currentContext!,
                    Routes.treeUpdate,
                    routeSettings: RouteSettings(
                      arguments: TreeUpdateArgument(
                        tree_id: widget.tree_id,
                        name: widget.name,
                        description: widget.description,
                      ),
                    ),
                  );
                  if (isUpdate) {
                    _refreshData();
                  }
                },
              ),
            ),
          ],
        ),
        SizedBox(height: 90),
      ],
    );
  }

  Future<void> _refreshData() async {
    _cubit!.getTreeDetail(widget.tree_id!);
  }
}

class TreeDetailArgument {
  String? tree_id;
  String? name;
  String? description;

  TreeDetailArgument({
    this.tree_id,
    this.name,
    this.description,
  });
}
