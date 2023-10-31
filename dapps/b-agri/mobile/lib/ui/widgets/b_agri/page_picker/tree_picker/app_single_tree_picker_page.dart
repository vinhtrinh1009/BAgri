import 'package:flutter/material.dart';
import 'package:flutter_base/blocs/app_cubit.dart';
import 'package:flutter_base/commons/app_colors.dart';

import 'package:flutter_base/models/entities/tree/list_tree_response.dart';
import 'package:flutter_base/models/enums/load_status.dart';

import 'package:flutter_base/ui/widgets/b_agri/app_bar_widget.dart';
import 'package:flutter_base/ui/widgets/b_agri/app_floating_action_button.dart';
import 'package:flutter_base/ui/widgets/b_agri/page_picker/garden_picker/app_garden_picker_page.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:flutter_html/shims/dart_ui.dart';

import '../../app_button.dart';
import '../../app_circular_progress_indicator.dart';

class AppSingleTreePickerPage extends StatefulWidget {
  final String? selectedTreeId;

  AppSingleTreePickerPage({this.selectedTreeId});

  @override
  _AppSingleTreePickerPageState createState() =>
      _AppSingleTreePickerPageState();
}

class _AppSingleTreePickerPageState extends State<AppSingleTreePickerPage> {
  late AppCubit _cubit;
  TreeEntity? selectedTree;

  @override
  void initState() {
    _cubit = BlocProvider.of<AppCubit>(context);
    super.initState();
    _cubit.fetchListTree();
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
          // List<TreeEntity> listTree = state.trees!.where((element) {
          //   if (element != null) {
          //     if (element.tree_id == widget.selectedTreeId) {
          //       return true;
          //     }
          //     return false;
          //   } else {
          //     return false;
          //   }
          // }).toList();

          return ListView.separated(
            padding: EdgeInsets.only(top: 10),
            itemCount: (state.trees)?.length ?? 0,
            shrinkWrap: true,
            primary: false,
            separatorBuilder: (context, index) {
              return SizedBox(height: 10);
            },
            itemBuilder: (context, index) {
              final tree = state.trees![index];
              String title = tree.name!;
              bool isSelected = false;
              if (widget.selectedTreeId != null) if (tree.tree_id ==
                  widget.selectedTreeId) isSelected = true;
              return ItemWidget(
                  title: title,
                  isSelected: isSelected,
                  onTap: () {
                    Navigator.of(context).pop(tree);
                  });
            },
          );
        }
      },
    );
  }
}
