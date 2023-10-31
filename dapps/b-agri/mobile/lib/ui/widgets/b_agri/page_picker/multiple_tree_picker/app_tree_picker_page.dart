import 'package:flutter/material.dart';
import 'package:flutter_base/blocs/app_cubit.dart';
import 'package:flutter_base/commons/app_colors.dart';

import 'package:flutter_base/models/entities/tree/list_tree_response.dart';
import 'package:flutter_base/models/enums/load_status.dart';

import 'package:flutter_base/ui/widgets/b_agri/app_bar_widget.dart';
import 'package:flutter_base/ui/widgets/b_agri/app_floating_action_button.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

import '../../app_button.dart';
import '../../app_circular_progress_indicator.dart';

class AppTreePickerPage extends StatefulWidget {
  final List<String> selectedTreeId;

  AppTreePickerPage({required this.selectedTreeId});

  @override
  _AppTreePickerPageState createState() => _AppTreePickerPageState();
}

class _AppTreePickerPageState extends State<AppTreePickerPage> {
  late AppCubit _cubit;
  List<TreeEntity> selectedTree = [];

  @override
  void initState() {
    _cubit = BlocProvider.of<AppCubit>(context);
    _cubit.fetchListTree();
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBarWidget(
        context: context,
        title: 'Chọn cây trồng',
      ),
      body: SafeArea(
        child: Column(
          children: [
            Expanded(child: _buildListResult()),
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                AppButton(
                  color: AppColors.redButton,
                  title: 'Hủy bỏ',
                  onPressed: () {
                    Navigator.of(context).pop();
                  },
                ),
                SizedBox(width: 50),
                AppButton(
                  width: 100,
                  color: AppColors.main,
                  title: 'Xác nhận',
                  onPressed: () async {
                    Navigator.of(context).pop(selectedTree);
                  },
                ),
              ],
            ),
            SizedBox(height: 50),
          ],
        ),
      ),
    );
  }

  Widget _buildListResult() {
    return BlocBuilder<AppCubit, AppState>(
      bloc: _cubit,
      buildWhen: (prev, current) {
        return prev.getTreeStatus != current.getTreeStatus;
      },
      builder: (context, state) {
        if (state.getTreeStatus == LoadStatus.LOADING) {
          return Center(
            child: AppCircularProgressIndicator(),
          );
        } else {
          return ListView.separated(
            itemCount: (state.trees)?.length ?? 0,
            shrinkWrap: true,
            primary: false,
            separatorBuilder: (context, index) {
              return Container(
                height: 1,
                color: Colors.grey.withOpacity(0.3),
                margin: EdgeInsets.symmetric(horizontal: 10),
              );
            },
            itemBuilder: (context, index) {
              final tree = state.trees![index];
              String title = tree.name!;
              bool isSelected = false;

              for (String e in widget.selectedTreeId) {
                if (e == tree.tree_id) {
                  isSelected = true;
                  selectedTree.add(tree);
                }
              }

              return ItemWidget(
                  title: title,
                  isSelected: isSelected,
                  onTap: (value) {
                    if (value) {
                      selectedTree.add(tree);
                    } else {
                      selectedTree.remove(tree);
                    }
                  });
            },
          );
        }
      },
    );
  }
}

class ItemWidget extends StatefulWidget {
  String title;
  bool isSelected;
  Function(bool value) onTap;
  ItemWidget({
    Key? key,
    required this.title,
    required this.isSelected,
    required this.onTap,
  }) : super(key: key);

  @override
  State<ItemWidget> createState() => _ItemWidgetState();
}

class _ItemWidgetState extends State<ItemWidget> {
  late bool check;
  @override
  void initState() {
    super.initState();
    check = widget.isSelected;
  }

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: () {
        setState(() {
          check = !check;
          widget.onTap(check);
        });
      },
      child: Container(
        color: Colors.white,
        padding: EdgeInsets.symmetric(horizontal: 12, vertical: 8),
        child: Row(
          children: [
            Expanded(
              flex: 8,
              child: Text(
                widget.title,
                overflow: TextOverflow.ellipsis,
              ),
            ),
            Visibility(
              visible: check,
              maintainSize: true,
              maintainAnimation: true,
              maintainState: true,
              child: Icon(
                Icons.check,
                color: AppColors.main,
              ),
            )
          ],
        ),
      ),
    );
  }
}
