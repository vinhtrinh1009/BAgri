import 'package:bloc/bloc.dart';
import 'package:equatable/equatable.dart';
import 'package:flutter_base/generated/l10n.dart';
import 'package:flutter_base/models/entities/garden/garden_entity.dart';
import 'package:flutter_base/models/entities/process/list_process.dart';
import 'package:flutter_base/models/entities/tree/list_tree_response.dart';
import 'package:flutter_base/models/enums/load_status.dart';
import 'package:flutter_base/repositories/process_repository.dart';
import 'package:flutter_base/repositories/tree_repository.dart';
import 'package:flutter_base/ui/widgets/app_snackbar.dart';

import 'package:rxdart/rxdart.dart';

part 'tree_listing_state.dart';

class TreeListCubit extends Cubit<TreeListState> {
  TreeRepository? treeRepository;

  TreeListCubit({this.treeRepository}) : super(TreeListState());

  final showMessageController = PublishSubject<SnackBarMessage>();

  @override
  Future<void> close() {
    showMessageController.close();
    return super.close();
  }

  void fetchListTree() async {
    emit(state.copyWith(getTreeStatus: LoadStatus.LOADING));
    try {
      final response = await treeRepository!.getListTreeData();
      if (response != null) {
        emit(state.copyWith(
          getTreeStatus: LoadStatus.SUCCESS,
          listData: response.data!.trees,
        ));
      } else {
        emit(state.copyWith(getTreeStatus: LoadStatus.FAILURE));
      }
      emit(state.copyWith(getTreeStatus: LoadStatus.SUCCESS));
    } catch (error) {
      emit(state.copyWith(getTreeStatus: LoadStatus.FAILURE));
    }
  }

  Future<void> deleteTree(String? treeId) async {
    emit(state.copyWith(deleteTreeStatus: LoadStatus.LOADING));
    try {
      final response = await treeRepository!.deleteTree(treeId: treeId);
      emit(state.copyWith(deleteTreeStatus: LoadStatus.SUCCESS));
    } catch (e) {
      emit(state.copyWith(deleteTreeStatus: LoadStatus.FAILURE));
      showMessageController.sink.add(SnackBarMessage(
        message: S.current.error_occurred,
        type: SnackBarType.ERROR,
      ));
      return;
    }
  }
}
