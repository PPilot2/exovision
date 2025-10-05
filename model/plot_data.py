import matplotlib.pyplot as plt
def plot_data(toi_filtered, td_filtered):
    # 1. Planet Radius vs Orbital Period
    plt.figure(figsize=(10, 6))
    plt.scatter(toi_filtered['pl_orbper'], toi_filtered['pl_rade'], 
            alpha=0.5, label='TOI', s=50, color='blue')
    plt.scatter(td_filtered['pl_orbper'], td_filtered['pl_rade'], 
            alpha=0.5, label='Overall', s=50, color='red')
    plt.xlabel('Orbital Period (days)')
    plt.ylabel('Planet Radius (Earth Radii)')
    plt.title('Planet Radius vs Orbital Period')
    plt.legend()
    plt.yscale('log')
    plt.xscale('log')
    plt.grid(True, alpha=0.3)
    plt.show()

    # 2. Stellar Temperature vs Planet Radius
    plt.figure(figsize=(10, 6))
    plt.scatter(toi_filtered['st_teff'], toi_filtered['pl_rade'],
            alpha=0.5, label=f'TOI (n={len(toi_filtered)})', s=50, color='blue')
    plt.scatter(td_filtered['st_teff'], td_filtered['pl_rade'],
            alpha=0.5, label=f'Overall (n={len(td_filtered)})', s=50, color='red')
    plt.xlabel('Stellar Temperature (K)')
    plt.ylabel('Planet Radius (Earth Radii)')
    plt.title('Planet Radius vs Stellar Temperature')
    plt.yscale('log')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.show()
    # 3. Stellar Temperature Distribution
    plt.figure(figsize=(10, 6))
    temp_data = [toi_filtered['st_teff'], td_filtered['st_teff']]
    plt.boxplot(temp_data, labels=['TOI', 'Overall'])
    plt.ylabel('Stellar Temperature (K)')
    plt.title('Stellar Temperature Distribution')
    plt.grid(True, alpha=0.3)
    plt.show()

    # 4. Planet Radius Distribution
    plt.figure(figsize=(10, 6))
    plt.hist(toi_filtered['pl_rade'], bins=50, alpha=0.5, 
            label=f'TOI (n={len(toi_filtered)})', density=True, color='blue')
    plt.hist(td_filtered['pl_rade'], bins=50, alpha=0.5, 
            label=f'Overall (n={len(td_filtered)})', density=True, color='red')
    plt.xlabel('Planet Radius (Earth Radii)')
    plt.ylabel('Density')
    plt.title('Planet Radius Distribution')
    plt.xlim(0, 10)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.show()
    # 5. Transit Duration vs Orbital Period
    plt.figure(figsize=(10, 6))
    plt.scatter(toi_filtered['pl_orbper'], toi_filtered['pl_trandur'],
            alpha=0.5, label=f'TOI (n={len(toi_filtered)})', s=50, color='blue')
    plt.scatter(td_filtered['pl_orbper'], td_filtered['pl_trandur'],
            alpha=0.5, label=f'Overall (n={len(td_filtered)})', s=50, color='red')
    plt.xlabel('Orbital Period (days)')
    plt.ylabel('Transit Duration (hours)')
    plt.title('Transit Duration vs Orbital Period')
    plt.xscale('log')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.show()

    # 6. Stellar Radius vs Planet Radius
    plt.figure(figsize=(10, 6))
    plt.scatter(toi_filtered['st_rad'], toi_filtered['pl_rade'],
            alpha=0.5, label='TESS', s=50, color='blue')
    plt.scatter(td_filtered['st_rad'], td_filtered['pl_rade'],
            alpha=0.5, label='Overall', s=50, color='red')
    plt.xlabel('Stellar Radius (Solar Radii)')
    plt.ylabel('Planet Radius (Earth Radii)')
    plt.title('Planet Size vs Star Size')
    plt.yscale('log')
    plt.xscale('log')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.show()

    # 7. Surface Gravity vs Transit Depth
    plt.figure(figsize=(10, 6))
    plt.scatter(toi_filtered['st_logg'], toi_filtered['pl_trandep'],
            alpha=0.5, label='TOI', s=50, color='blue')
    plt.scatter(td_filtered['st_logg'], td_filtered['pl_trandep'],
            alpha=0.5, label='Overall', s=50, color='red')
    plt.xlabel('Stellar Surface Gravity (log g)')
    plt.ylabel('Transit Depth')
    plt.title('Transit Depth vs Surface Gravity')
    plt.yscale('log')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.show()

    # 8. Feature Correlation Matrix
    features = ['pl_orbper', 'pl_rade', 'st_teff', 'pl_trandep', 
                'pl_trandur', 'st_rad', 'st_logg']
    
    # TESS correlations
    plt.figure(figsize=(12, 10))
    correlation_tess = toi_filtered[features].corr()
    plt.imshow(correlation_tess, cmap='coolwarm', aspect='auto')
    plt.colorbar()
    plt.xticks(range(len(features)), features, rotation=45)
    plt.yticks(range(len(features)), features)
    plt.title('TESS Feature Correlations')
    for i in range(len(features)):
        for j in range(len(features)):
            plt.text(j, i, f'{correlation_tess.iloc[i, j]:.2f}',
                    ha='center', va='center')
    plt.tight_layout()
    plt.show()


    