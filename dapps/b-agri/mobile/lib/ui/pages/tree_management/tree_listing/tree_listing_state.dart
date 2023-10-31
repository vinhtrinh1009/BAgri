part of 'tree_listing_cubit.dart';

class TreeListState extends Equatable {
  LoadStatus? getTreeStatus;
  LoadStatus? deleteTreeStatus;
  List<TreeEntity>? listData;

  TreeListState({this.getTreeStatus, this.listData, this.deleteTreeStatus});

  TreeListState copyWith({
    LoadStatus? getTreeStatus,
    List<TreeEntity>? listData,
    LoadStatus? deleteTreeStatus,
  }) {
    return TreeListState(
      getTreeStatus: getTreeStatus ?? this.getTreeStatus,
      listData: listData ?? this.listData,
      deleteTreeStatus: deleteTreeStatus ?? this.deleteTreeStatus,
    );
  }

  @override
  List<Object?> get props =>
      [this.getTreeStatus, this.listData, this.deleteTreeStatus];
}
