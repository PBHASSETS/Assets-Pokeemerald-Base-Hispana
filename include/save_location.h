#ifndef GUARD_SAVE_LOCATION_H
#define GUARD_SAVE_LOCATION_H

// specialSaveWarp flags
#define CONTINUE_GAME_WARP           (1 << 0)
#define POKECENTER_SAVEWARP          (1 << 1)
#define LOBBY_SAVEWARP               (1 << 2)
//
//
//
//
#define CHAMPION_SAVEWARP            (1 << 7)

void TrySetMapSaveWarpStatus(void);
void SetChampionSaveWarp(void);

#endif // GUARD_SAVE_LOCATION_H
