from SMSA.audio_domain.AudioPelt import AudioPelt


if __name__ == "__main__":
    model = AudioPelt(algo_type='pelt', n_bkps_from_gt=False)
    print(model.predict("/Users/21415968/Desktop/diploma/symbolic-music-structure-analysis/BPS_FH_Dataset/1/1.mp3"))
