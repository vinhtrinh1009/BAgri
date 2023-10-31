part of 'season_detail_cubit.dart';

class SeasonDetailState extends Equatable {
  LoadStatus? loadStatus;
  SeasonEntity? season;
  String? linkQR;
  String? linkUrl;
  @override
  List<dynamic> get props => [
        loadStatus,
        season,
        linkQR,
        linkUrl,
      ];

  SeasonDetailState({
    this.loadStatus,
    this.season,
    this.linkQR,
    this.linkUrl,
  });

  SeasonDetailState copyWith({
    LoadStatus? loadStatus,
    SeasonEntity? season,
    String? linkQR,
    String? linkUrl,
  }) {
    return SeasonDetailState(
      loadStatus: loadStatus ?? this.loadStatus,
      season: season ?? this.season,
      linkQR: linkQR ?? this.linkQR,
      linkUrl: linkUrl ?? this.linkUrl,
    );
  }
}
