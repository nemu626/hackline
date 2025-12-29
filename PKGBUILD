# Maintainer: nemu626 <nemu626.log@gmail.com>
pkgname=ttf-hackline-nerd-git
_pkgname=hackline
pkgver=r2.26164f9
pkgrel=1
pkgdesc="A programming font that combines Hack and LINE Seed Font, with support for Japanese and Korean (including Nerd Fonts)."
arch=('any')
url="https://github.com/nemu626/hackline"
license=('OFL')
depends=('fontconfig')
makedepends=('git' 'python-fonttools' 'unzip')
provides=("${_pkgname}")
conflicts=("${_pkgname}")
source=("git+${url}.git")
sha256sums=('SKIP')

pkgver() {
  cd "$srcdir/${_pkgname}"
  printf "r%s.%s" "$(git rev-list --count HEAD)" "$(git rev-parse --short HEAD)"
}

build() {
  cd "$srcdir/${_pkgname}"
  ./build.sh --nerd
}

package() {
  cd "$srcdir/${_pkgname}"
  install -d "${pkgdir}/usr/share/fonts/TTF"
  install -d "${pkgdir}/usr/share/licenses/${pkgname}"
  install -m644 build/*.ttf "${pkgdir}/usr/share/fonts/TTF/"
  install -m644 LICENSE "${pkgdir}/usr/share/licenses/${pkgname}/"
}
